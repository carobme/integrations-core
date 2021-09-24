# (C) Datadog, Inc. 2021-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import fcntl
import os
import subprocess
import sys
import time
from datetime import datetime
from typing import List, NamedTuple, Tuple

from datadog_checks.base import AgentCheck
from datadog_checks.base.utils.db import QueryManager
from datadog_checks.base.utils.serialization import json

from . import queries
from .config_models import ConfigMixin

SystemInfo = NamedTuple('SystemInfo', [('hostname', str), ('os_version', int), ('os_release', int)])


class IbmICheck(AgentCheck, ConfigMixin):
    SERVICE_CHECK_NAME = "ibm_i.can_connect"

    def __init__(self, name, init_config, instances):
        super(IbmICheck, self).__init__(name, init_config, instances)

        self._connection_string = None
        self._subprocess = None
        self._query_manager = None
        self._current_errors = 0
        self.check_initializations.append(self.set_up_query_manager)

    def check(self, _):
        self._current_errors = 0

        try:
            self.query_manager.execute()
            check_status = AgentCheck.OK
        except AttributeError:
            self.warning('Could not set up query manager, skipping check run')
            check_status = None
        except Exception as e:
            self._delete_connection_subprocess(e)
            check_status = AgentCheck.CRITICAL

        # At least one query failed, set the service check as failing
        if self._current_errors:
            check_status = AgentCheck.CRITICAL

        if check_status is not None:
            self.service_check(
                self.SERVICE_CHECK_NAME,
                check_status,
                tags=self.config.tags,
                hostname=self._query_manager.hostname,
            )

    def cancel(self):
        # When the check gets cancelled, clean up the connection subprocess.
        self._delete_connection_subprocess()

    def handle_query_error(self, error):
        self._current_errors += 1
        return error

    @property
    def connection_subprocess(self):
        if self._subprocess is None:
            self._create_connection_subprocess()
        return self._subprocess

    def _create_connection_subprocess(self):
        self._subprocess = subprocess.Popen(
            [
                sys.executable,
                "-c",
                "from datadog_checks.ibm_i.query_script import query; query()",
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Set stdout reader as non-blocking, we don't want to
        # block .read() calls to be able to time out.
        fl = fcntl.fcntl(self._subprocess.stdout.fileno(), fcntl.F_GETFL)
        fcntl.fcntl(self._subprocess.stdout, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        # Set stderr reader as non-blocking, we don't want to
        # wait until EOF is sent, we only want to read whatever is there when
        # we try to return errors.
        fl = fcntl.fcntl(self._subprocess.stderr.fileno(), fcntl.F_GETFL)
        fcntl.fcntl(self._subprocess.stderr, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        try:
            print(self.connection_string, file=self._subprocess.stdin, flush=True)
        except BrokenPipeError as e:
            # The stdin pipe is broken, usually due to the Agent
            # killing the subprocess when stopping.
            # Clean up then return.
            self._delete_connection_subprocess(e)

    def _delete_connection_subprocess(self, message):
        if self._subprocess:
            self.log.debug("Deleting connection: %s", message)
            while not self._subprocess.returncode:
                self._subprocess.kill()
                self._subprocess.wait()

        self._subprocess = None

    def execute_query(self, query, disconnect_on_error=True):
        try:
            # Write query
            print(query['text'], file=self.connection_subprocess.stdin, flush=True)
        except BrokenPipeError as e:
            # The stdin pipe is broken, usually due to the Agent
            # killing the subprocess when stopping.
            # Clean up then return.
            self._delete_connection_subprocess(e)
            return

        done = False
        query_start = datetime.now()

        while not done and (datetime.now() - query_start).total_seconds() <= query['timeout']:
            # Sleep for a bit to wait for results & avoid being a busy loop
            time.sleep(0.2)
            try:
                # To avoid blocking never use a pipe's file descriptor iterator. See https://bugs.python.org/issue3907
                for line in iter(self.connection_subprocess.stdout.readline, ''):
                    stripped_line = line.strip()
                    if stripped_line == "":
                        # Empty line, skip
                        continue
                    if stripped_line == "ENDOFQUERY":
                        done = True
                        break
                    try:
                        yield json.loads(stripped_line)
                    except Exception as e:
                        # We didn't manage to parse the line provided by the subprocess
                        # Remove subprocess to restart on a clean state and raise.
                        self._delete_connection_subprocess(e)
                        raise
            except TypeError:
                # We couldn't read anything
                continue
            except BrokenPipeError as e:
                # The stdout pipe is broken, usually due to the Agent
                # killing the subprocess when stopping.
                # Clean up then return.
                self._delete_connection_subprocess(e)
                return

        e = None
        try:
            e = self.connection_subprocess.stderr.read().strip()
        except TypeError:
            # We couldn't read anything
            pass
        except BrokenPipeError as e:
            # The stderr pipe is broken, usually due to the Agent
            # killing the subprocess when stopping.
            # Clean up then return.
            self._delete_connection_subprocess(e)
            return

        # disconnect_on_error can be set to False for queries we
        # expect to fail and where we don't want to disconnect.
        if e:
            if disconnect_on_error:
                self._delete_connection_subprocess(e)
            raise Exception(e)

        if not done:
            if disconnect_on_error:
                self._delete_connection_subprocess("Timed out after {} seconds".format(query['timeout']))
            raise Exception("Timed out after {} seconds".format(query['timeout']))

    @property
    def connection_string(self):
        if self._connection_string is None:
            # https://www.connectionstrings.com/as-400/
            # https://www.ibm.com/support/pages/odbc-driver-ibm-i-access-client-solutions
            connection_string = self.config.connection_string
            if not connection_string:
                connection_string = f'Driver={{{self.config.driver.strip("{}")}}};'

                if self.config.system:
                    connection_string += f'System={self.config.system};'

                if self.config.username:
                    connection_string += f'UID={self.config.username};'

                if self.config.password:
                    connection_string += f'PWD={self.config.password};'
                    self.register_secret(self.config.password)

            self._connection_string = connection_string

        return self._connection_string

    @property
    def query_manager(self):
        if self._query_manager is None:
            self.set_up_query_manager()
        return self._query_manager

    def set_up_query_manager(self):
        system_info = self.fetch_system_info()
        if system_info:
            query_list = [
                queries.get_cpu_usage(self.config.query_timeout),
                queries.get_jobq_job_status(self.config.job_query_timeout),
                queries.get_active_job_status(self.config.job_query_timeout),
                queries.get_job_memory_usage(self.config.job_query_timeout),
                queries.get_memory_info(self.config.query_timeout),
                queries.get_job_queue_info(self.config.query_timeout),
                queries.get_message_queue_info(self.config.system_mq_query_timeout, self.config.severity_threshold),
            ]

            if system_info.os_version > 7 or (system_info.os_version == 7 and system_info.os_release >= 3):
                query_list.append(queries.get_base_disk_usage_73(self.config.query_timeout))
                query_list.append(queries.get_disk_usage(self.config.query_timeout))
                query_list.append(queries.get_subsystem_info(self.config.query_timeout))
            else:
                query_list.append(queries.get_base_disk_usage_72(self.config.query_timeout))

            self._query_manager = QueryManager(
                self,
                self.execute_query,
                tags=self.config.tags,
                queries=query_list,
                hostname=system_info.hostname,
                error_handler=self.handle_query_error,
            )
            self._query_manager.compile_queries()

    def fetch_system_info(self):
        try:
            return self.system_info_query()
        except Exception:
            # In case of errors, the connection will have already been cleaned by execute_query.
            pass

    def system_info_query(self):
        query = {
            'text': "SELECT HOST_NAME, OS_VERSION, OS_RELEASE FROM SYSIBMADM.ENV_SYS_INFO",
            'timeout': self.config.query_timeout,
        }
        results = list(self.execute_query(query))  # type: List[Tuple[str]]
        if len(results) == 0:
            self.log.error("Couldn't find system info on the remote system.")
            return None
        if len(results) > 1:
            self.log.error("Too many results returned by system query. Expected 1, got %d", len(results))
            return None

        info_row = results[0]
        if len(info_row) != 3:
            self.log.error("Expected 3 columns in system info query, got %d", len(info_row))
            return None

        hostname = info_row[0]
        try:
            os_version = int(info_row[1])
        except ValueError:
            self.log.error("Expected integer for OS version, got %s", info_row[1])
            return None

        try:
            os_release = int(info_row[2])
        except ValueError:
            self.log.error("Expected integer for OS release, got %s", info_row[2])
            return None

        return SystemInfo(hostname=hostname, os_version=os_version, os_release=os_release)
# (C) Datadog, Inc. 2019-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os
from copy import deepcopy

import pytest
import vertica_python as vertica

from datadog_checks.dev import LazyFunction, docker_run

from . import common


class InitializeDB(LazyFunction):
    def __init__(self, config):
        self.conn_info = {
            'database': config['db'],
            'host': config['server'],
            'port': config['port'],
            'user': config['username'],
            'password': config['password'],
            'connection_timeout': config['timeout'],
        }

    def __call__(self):
        with vertica.connect(**self.conn_info) as conn:
            cur = conn.cursor()

            # Create data
            cur.execute('CREATE TABLE {} (a INT, b VARCHAR(32))'.format(common.ID))
            cur.execute("INSERT INTO {} (a, b) VALUES (9000, 'DBZ')".format(common.ID))
            conn.commit()

            # Trigger an audit
            cur.execute('SELECT AUDIT_LICENSE_SIZE()')


@pytest.fixture(scope='session')
def dd_environment():
    compose_file = get_compose_file(os.environ['VERTICA_VERSION'])

    with docker_run(compose_file, log_patterns=['Vertica is now running'], conditions=[InitializeDB(common.CONFIG)]):
        yield common.CONFIG


@pytest.fixture
def instance():
    return deepcopy(common.CONFIG)


@pytest.fixture
def tls_instance():
    return deepcopy(common.TLS_CONFIG)


@pytest.fixture
def tls_instance_legacy():
    return deepcopy(common.TLS_CONFIG_LEGACY)


def get_compose_file(vertica_version):
    major_version = int(vertica_version.split('.', 1)[0])

    if major_version < 10:
        fname = 'docker-compose-9.yaml'
    else:
        fname = 'docker-compose.yaml'

    return os.path.join(common.HERE, 'docker', fname)

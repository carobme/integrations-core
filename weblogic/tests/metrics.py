# (C) Datadog, Inc. 2021-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from datadog_checks.dev.jmx import JVM_E2E_METRICS_NEW

METRICS = [
    "weblogic.connector_connection_pool_runtime.connections_active",
    "weblogic.connector_connection_pool_runtime.connections_free",
    "weblogic.connector_connection_pool_runtime.connections_created_total",
    "weblogic.jms_runtime.connections_current",
    "weblogic.jms_runtime.connections_total",
    "weblogic.jms_runtime.jms_servers",
    "weblogic.jms_runtime.jms_servers_total",
    "weblogic.jvm_runtime.heap_size",
    "weblogic.jvm_runtime.heap_free",
    "weblogic.jvm_runtime.heap_free_percent",
    "weblogic.jvm_runtime.heap_size_max",
    "weblogic.server_runtime.open_sockets",
    "weblogic.server.threadpool_socket_readers_percent",
    "weblogic.server.max_open_sockets",
    "weblogic.server_channel_runtime.sockets_accepted",
    "weblogic.server_channel_runtime.connections_active",
    "weblogic.server_channel_runtime.bytes_received",
    "weblogic.server_channel_runtime.bytes_sent",
    "weblogic.server_channel_runtime.messages_received",
    "weblogic.server_channel_runtime.messages_sent",
    "weblogic.threadpool_runtime.completed_requests",
    "weblogic.threadpool_runtime.execute_threads_idle",
    "weblogic.threadpool_runtime.execute_threads_total",
    "weblogic.threadpool_runtime.user_requests_pending",
    "weblogic.threadpool_runtime.threads_hogging",
    "weblogic.threadpool_runtime.overload_rejected_requests",
    "weblogic.threadpool_runtime.queue_length",
    "weblogic.threadpool_runtime.shared_capacity_work_managers",
    "weblogic.threadpool_runtime.threads_standby",
    "weblogic.threadpool_runtime.threads_stuck",
    "weblogic.threadpool_runtime.throughput",
    "weblogic.work_manager_runtime.requests_completed",
    "weblogic.work_manager_runtime.requests_pending",
    "weblogic.work_manager_runtime.threads_stuck",
    "weblogic.servlet_runtime.exec_time_high",
    "weblogic.servlet_runtime.exec_time_low",
    "weblogic.servlet_runtime.reloads_total",
    "weblogic.servlet_runtime.pool_max_capacity",
    "weblogic.webapp_component_runtime.sessions_current",
] + JVM_E2E_METRICS_NEW
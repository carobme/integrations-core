# (C) Datadog, Inc. 2018-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import os

from datadog_checks.base.utils.common import get_docker_hostname

HERE = os.path.dirname(os.path.abspath(__file__))
HOST = get_docker_hostname()
PORT = 8002
API_URL = "http://{}:{}".format(HOST, PORT)
USERNAME = 'admin'
PASSWORD = 'admin'

INSTANCE = {
    'url': API_URL,
    'username': USERNAME,
    'password': PASSWORD,
    'auth_type': 'digest',
}


CHECK_CONFIG = {
    'init_config': {},
    'instances': [INSTANCE],
}


METRICS = [
    'marklogic.forests.backup-count',
    'marklogic.forests.max-stands-per-forest',
    'marklogic.forests.merge-count',
    'marklogic.forests.restore-count',
    'marklogic.forests.state-not-open',
    'marklogic.forests.total-forests',
    'marklogic.hosts.memory-process-huge-pages-size',
    'marklogic.hosts.memory-process-rss',
    'marklogic.hosts.memory-size',
    'marklogic.hosts.memory-system-free',
    'marklogic.hosts.memory-system-total',
    'marklogic.hosts.total-cpu-stat-system',
    'marklogic.hosts.total-cpu-stat-user',
    'marklogic.hosts.total-hosts',
    'marklogic.hosts.total-hosts-offline',
    'marklogic.requests.max-seconds',
    'marklogic.requests.mean-seconds',
    'marklogic.requests.median-seconds',
    'marklogic.requests.min-seconds',
    'marklogic.requests.ninetieth-percentile-seconds',
    'marklogic.requests.query-count',
    'marklogic.requests.standard-dev-seconds',
    'marklogic.requests.total-requests',
    'marklogic.requests.update-count',
    'marklogic.servers.expanded-tree-cache-hit-rate',
    'marklogic.servers.expanded-tree-cache-miss-rate',
    'marklogic.servers.request-count',
    'marklogic.servers.request-rate',
    'marklogic.transactions.max-seconds',
    'marklogic.transactions.mean-seconds',
    'marklogic.transactions.median-seconds',
    'marklogic.transactions.min-seconds',
    'marklogic.transactions.ninetieth-percentile-seconds',
    'marklogic.transactions.standard-dev-seconds',
    'marklogic.transactions.total-transactions',
    'marklogic.hosts.backup-read-load',
    'marklogic.hosts.backup-read-rate',
    'marklogic.hosts.backup-write-load',
    'marklogic.hosts.backup-write-rate',
    'marklogic.hosts.deadlock-rate',
    'marklogic.hosts.deadlock-wait-load',
    'marklogic.hosts.external-binary-read-load',
    'marklogic.hosts.external-binary-read-rate',
    'marklogic.hosts.foreign-xdqp-client-receive-load',
    'marklogic.hosts.foreign-xdqp-client-receive-rate',
    'marklogic.hosts.foreign-xdqp-client-send-load',
    'marklogic.hosts.foreign-xdqp-client-send-rate',
    'marklogic.hosts.foreign-xdqp-server-receive-load',
    'marklogic.hosts.foreign-xdqp-server-receive-rate',
    'marklogic.hosts.foreign-xdqp-server-send-load',
    'marklogic.hosts.foreign-xdqp-server-send-rate',
    'marklogic.hosts.journal-write-load',
    'marklogic.hosts.journal-write-rate',
    'marklogic.hosts.large-read-load',
    'marklogic.hosts.large-read-rate',
    'marklogic.hosts.large-write-load',
    'marklogic.hosts.large-write-rate',
    'marklogic.hosts.memory-process-swap-rate',
    'marklogic.hosts.memory-system-pagein-rate',
    'marklogic.hosts.memory-system-pageout-rate',
    'marklogic.hosts.memory-system-swapin-rate',
    'marklogic.hosts.memory-system-swapout-rate',
    'marklogic.hosts.merge-read-load',
    'marklogic.hosts.merge-read-rate',
    'marklogic.hosts.merge-write-load',
    'marklogic.hosts.merge-write-rate',
    'marklogic.hosts.query-read-load',
    'marklogic.hosts.query-read-rate',
    'marklogic.hosts.read-lock-hold-load',
    'marklogic.hosts.read-lock-rate',
    'marklogic.hosts.read-lock-wait-load',
    'marklogic.hosts.restore-read-load',
    'marklogic.hosts.restore-read-rate',
    'marklogic.hosts.restore-write-load',
    'marklogic.hosts.restore-write-rate',
    'marklogic.hosts.save-write-load',
    'marklogic.hosts.save-write-rate',
    'marklogic.hosts.total-load',
    'marklogic.hosts.total-rate',
    'marklogic.hosts.write-lock-hold-load',
    'marklogic.hosts.write-lock-rate',
    'marklogic.hosts.write-lock-wait-load',
    'marklogic.hosts.xdqp-client-receive-load',
    'marklogic.hosts.xdqp-client-receive-rate',
    'marklogic.hosts.xdqp-client-send-load',
    'marklogic.hosts.xdqp-client-send-rate',
    'marklogic.hosts.xdqp-server-receive-load',
    'marklogic.hosts.xdqp-server-receive-rate',
    'marklogic.hosts.xdqp-server-send-load',
    'marklogic.hosts.xdqp-server-send-rate',
]

# (C) Datadog, Inc. 2021-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

# This file is autogenerated.
# To change this file you should edit assets/configuration/spec.yaml and then run the following commands:
#     ddev -x validate config -s <INTEGRATION_NAME>
#     ddev -x validate models -s <INTEGRATION_NAME>

from datadog_checks.base.utils.models.fields import get_default_field_value


def shared_kafka_timeout(field, value):
    return 5


def shared_service(field, value):
    return get_default_field_value(field, value)


def shared_zk_timeout(field, value):
    return 5


def instance_broker_requests_batch_size(field, value):
    return 30


def instance_consumer_groups(field, value):
    return get_default_field_value(field, value)


def instance_disable_generic_tags(field, value):
    return False


def instance_empty_default_hostname(field, value):
    return False


def instance_kafka_client_api_version(field, value):
    return get_default_field_value(field, value)


def instance_kafka_consumer_offsets(field, value):
    return False


def instance_metric_patterns(field, value):
    return get_default_field_value(field, value)


def instance_min_collection_interval(field, value):
    return 15


def instance_monitor_all_broker_highwatermarks(field, value):
    return False


def instance_monitor_unlisted_consumer_groups(field, value):
    return False


def instance_sasl_kerberos_domain_name(field, value):
    return get_default_field_value(field, value)


def instance_sasl_kerberos_service_name(field, value):
    return 'kafka'


def instance_sasl_mechanism(field, value):
    return get_default_field_value(field, value)


def instance_sasl_plain_password(field, value):
    return get_default_field_value(field, value)


def instance_sasl_plain_username(field, value):
    return get_default_field_value(field, value)


def instance_security_protocol(field, value):
    return 'PLAINTEXT'


def instance_service(field, value):
    return get_default_field_value(field, value)


def instance_tags(field, value):
    return get_default_field_value(field, value)


def instance_tls_ca_cert(field, value):
    return get_default_field_value(field, value)


def instance_tls_cert(field, value):
    return get_default_field_value(field, value)


def instance_tls_crlfile(field, value):
    return get_default_field_value(field, value)


def instance_tls_private_key(field, value):
    return get_default_field_value(field, value)


def instance_tls_private_key_password(field, value):
    return get_default_field_value(field, value)


def instance_tls_validate_hostname(field, value):
    return True


def instance_tls_verify(field, value):
    return True


def instance_zk_connect_str(field, value):
    return get_default_field_value(field, value)


def instance_zk_prefix(field, value):
    return get_default_field_value(field, value)

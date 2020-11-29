# -*- coding: utf-8 -*-
"""Various functions for ib brokers."""
from modules.iib_api import get_status


def get_metric_name(metric_label):
    """Returns pushgateway formatted metric name."""
    return 'ib_broker_{0}'.format(metric_label)


def get_metric_annotation():
    """Returns dictionary with annotations 'HELP' and 'TYPE' for metrics."""
    annotations = {
        'status': '# HELP {0} Current status of IB broker.\n\
# TYPE {0} gauge\n'.format(get_metric_name('status'))}
    return annotations


def get_brokers_status(brokers_data):
    """Returns list with statuses for brokers."""
    output_list = brokers_data.split('\n')
    brokers = list()
    for record in filter(None, output_list):
        record_list = record.split()
        broker_name = record_list[2].replace("'", "")
        qm_name = record_list[6].replace("'", "")
        status = record_list[8].replace("'", "").replace(".", "")
        brokers.append([broker_name, status, qm_name])
    return brokers


def get_broker_items(broker_row_data):
    """Returns lists with data for broker items: execution groups, applications, message flows."""
    output_list = broker_row_data.split('\n')
    exec_groups = list()
    applications = list()
    message_flows = list()
    # See IBM diagnostic messages:
    # https://www.ibm.com/support/knowledgecenter/en/SSMKHH_9.0.0/com.ibm.etools.mft.bipmsgs.doc/ay_bip1.htm
    # Also you can use command: mqsiexplain <bip_code>
    bip_codes = {
     'BIP1286I': exec_groups,
     'BIP1287I': exec_groups,
     'BIP1275I': applications,
     'BIP1276I': applications,
     'BIP1277I': message_flows,
     'BIP1278I': message_flows}
    for record in output_list:
        if record:
            bip_code = record.split()[0].replace(':', '')
            if bip_code in bip_codes.keys():
                bip_codes[bip_code].append(record)
    return exec_groups, applications, message_flows


def format_broker(broker_name, status, qm_name):
    """Returns string with all metrics for broker which ready to push to pushgateway."""
    metrics_annotation = get_metric_annotation()
    template_string = 'brokername="{0}", qmname="{1}"'.format(
        broker_name,
        qm_name)
    broker_metric = '{0}{{{1}}} {2}\n'.format(
        get_metric_name(metric_label='status'),
        template_string,
        get_status(status=status))
    broker_metric = '{0}{1}'.format(
        metrics_annotation['status'],
        broker_metric)
    return broker_metric

# -*- coding: utf-8 -*-
"""Various functions for ib message flows."""
from modules.iib_api import get_status


def get_metric_name(metric_label):
    """Returns pushgateway formatted metric name."""
    return 'ib_message_flow_{0}'.format(metric_label)


def get_metric_annotation():
    """Returns dictionary with annotations 'HELP' and 'TYPE' for metrics."""
    annotations = {
        'status': '# HELP {0} Current status of IB message flow.\n\
# TYPE {0} gauge\n'.format(get_metric_name('status'))}
    return annotations


def format_message_flows(message_flows, broker_name):
    """Returns string with all metrics for all message flows which ready to push to pushgateway."""
    metrics_annotation = get_metric_annotation()
    msg_flow_metric_data = str()
    for msg_flow in message_flows:
        msg_flow_list = msg_flow.split()
        egname, app_name, message_flow_name, status = msg_flow_list[7], msg_flow_list[11], msg_flow_list[3], msg_flow_list[9].replace(".", "")
        template_string = 'egname="{0}", brokername="{1}", appname="{2}", messageflowname="{3}"'.format(
            egname.replace("'", ""),
            broker_name,
            app_name.replace("'", "").replace(",", ""),
            message_flow_name.replace("'", ""))
        msg_flow_metric = '{0}{{{1}}} {2}\n'.format(
            get_metric_name(metric_label='status'),
            template_string,
            get_status(status=status))
        msg_flow_metric_data += msg_flow_metric
    msg_flow_metric_data = '{0}{1}'.format(
        metrics_annotation['status'],
        msg_flow_metric_data)
    return msg_flow_metric_data

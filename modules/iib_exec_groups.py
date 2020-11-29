# -*- coding: utf-8 -*-
"""Various functions for ib execution groups."""
from modules.iib_api import get_status


def get_metric_name(metric_label):
    """Returns pushgateway formatted metric name."""
    return 'ib_exec_group_{0}'.format(metric_label)


def get_metric_annotation():
    """Returns dictionary with annotations 'HELP' and 'TYPE' for metrics."""
    annotations = {
        'status': '# HELP {0} Current status of IB execution group.\n\
# TYPE {0} gauge\n'.format(get_metric_name('status'))}
    return annotations


def format_exec_groups(exec_groups):
    """Returns string with all metrics for all execution groups which ready to push to pushgateway."""
    metrics_annotation = get_metric_annotation()
    eg_metric_data = str()
    for eg in exec_groups:
        eg_list = eg.split()
        broker_name, egname, status = eg_list[6], eg_list[3], eg_list[8].replace(".", "")
        template_string = 'brokername="{0}", egname="{1}"'.format(
            broker_name.replace("'", ""),
            egname.replace("'", ""))
        eg_metric = '{0}{{{1}}} {2}\n'.format(
            get_metric_name(metric_label='status'),
            template_string,
            get_status(status=status))
        eg_metric_data += eg_metric
    eg_metric_data = '{0}{1}'.format(
        metrics_annotation['status'],
        eg_metric_data)
    return eg_metric_data

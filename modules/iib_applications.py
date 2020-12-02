# -*- coding: utf-8 -*-
"""Various functions for ib applications."""
from modules.iib_api import get_status


def get_metric_name(metric_label):
    """Returns pushgateway formatted metric name."""
    return 'ib_application_{0}'.format(metric_label)


def get_metric_annotation():
    """Returns dictionary with annotations 'HELP' and 'TYPE' for metrics."""
    annotations = {
        'status': '# HELP {0} Current status of IB application.\n\
# TYPE {0} gauge\n'.format(get_metric_name('status'))}
    return annotations


def format_applications(applications, broker_name, bip_codes):
    """Returns string with all metrics for all applications which ready to push to pushgateway."""
    metrics_annotation = get_metric_annotation()
    app_metric_data = str()
    for app in applications:
        app_list = app.split()
        bip_code = app_list[0].replace(':', '')
        if bip_code in bip_codes.keys():
            egname = app_list[bip_codes[bip_code][1]]
            app_name = app_list[bip_codes[bip_code][2]]
            status = app_list[bip_codes[bip_code][3]].replace(".", "")
            template_string = 'egname="{0}", brokername="{1}", appname="{2}"'.format(
                egname.replace("'", ""),
                broker_name,
                app_name.replace("'", ""))
            app_metric = '{0}{{{1}}} {2}\n'.format(
                get_metric_name(metric_label='status'),
                template_string,
                get_status(status=status))
            app_metric_data += app_metric
    if app_metric_data:
        app_metric_data = '{0}{1}'.format(
            metrics_annotation['status'],
            app_metric_data)
    return app_metric_data

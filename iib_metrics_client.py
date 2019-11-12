#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from log.logger_client import set_logger
from requests import ConnectionError
from urllib3.exceptions import ResponseError
import sys
import traceback
import platform
import time
from modules.iib_api import run_iib_command


logger = set_logger()

STATUS_MAP = {
    'running.': 1,
    'stopped.': 0
    }


class PrometheusBadResponse(Exception):
    pass


def put_metric_to_gateway(metric_data, job):
    hostname = platform.node()
    port = 9091
    src_url = "http://{0}:{1}".format(hostname, port)
    headers = {"Content-Type": "text/plain; version=0.0.4"}
    dest_url = "{0}/metrics/job/{1}".format(src_url, job)
    logger.info("Destination url: {0}".format(dest_url))
    logger.info("Metric data to push: {0}".format(metric_data))
    try:
        response = requests.put(dest_url, data=metric_data, headers=headers)
        if not response.ok:
            raise PrometheusBadResponse("Bad response - {0} \
            from {1}\nResponseText: {2}".format(
                response,
                dest_url,
                response.text
            ))
        logger.info("Success! Server response: {0}".format(response))
    except (ConnectionError, ResponseError):
        raise PrometheusBadResponse("{0} is not available!".format(dest_url))


def get_brokers_status(brokers_data):
    output_list = brokers_data.split('\n')
    brokers = []
    for record in filter(None, output_list):
        record_list = record.split()
        broker_name = record_list[2].replace("'", "")
        qm_name = record_list[6].replace("'", "")
        status = record_list[8].replace("'", "")
        brokers.append([broker_name, status, qm_name])
    return brokers


def get_broker_items(broker_row_data):
    output_list = broker_row_data.split('\n')
    exec_groups = []
    applications = []
    message_flows = []
    # See IBM diagnostic messages:
    # https://www.ibm.com/support/knowledgecenter/en/SSMKHH_9.0.0/com.ibm.etools.mft.bipmsgs.doc/ay_bip1.htm
    # Also you can use command: mqsiexplain <bip_code>
    bip_codes = {
     'BIP1286I': exec_groups,
     'BIP1287I': exec_groups,
     'BIP1275I': applications,
     'BIP1276I': applications,
     'BIP1277I': message_flows,
     'BIP1278I': message_flows
    }
    for record in output_list:
        if record:
            bip_code = record.split()[0].replace(':', '')
            if bip_code in bip_codes.keys():
                bip_codes[bip_code].append(record)
    return exec_groups, applications, message_flows


def format_broker(broker_name, status, qm_name):
    broker_metric = 'ib_broker_status{brokername="%s", qmname="%s"} %d\n' % (
            broker_name,
            qm_name,
            STATUS_MAP[status]
            )
    return broker_metric


def format_applications(applications, broker_name):
    app_metric_data = ''
    for app in applications:
        app_list = app.split()
        egname, app_name, status = app_list[6], app_list[2], app_list[8]
        app_metric = 'ib_application_status{egname="%s", brokername="%s", appname="%s"} %d\n' % (
            egname.replace("'", ""),
            broker_name,
            app_name.replace("'", ""),
            STATUS_MAP[status]
            )
        app_metric_data += app_metric
    return app_metric_data


def format_exec_groups(exec_groups):
    eg_metric_data = ''
    for eg in exec_groups:
        eg_list = eg.split()
        broker_name, egname, status = eg_list[6], eg_list[3], eg_list[8]
        eg_metric = 'ib_exec_group_status{brokername="%s", egname="%s"} %d\n' % (
            broker_name.replace("'", ""),
            egname.replace("'", ""),
            STATUS_MAP[status]
            )
        eg_metric_data += eg_metric
    return eg_metric_data


def format_message_flows(message_flows, broker_name):
    msg_flow_metric_data = ''
    for msg_flow in message_flows:
        msg_flow_list = msg_flow.split()
        egname, app_name, message_flow_name, status = msg_flow_list[7], msg_flow_list[11], msg_flow_list[3], msg_flow_list[9]
        msg_flow_metric = 'ib_message_flow_status{egname="%s", brokername="%s", appname="%s", messageflowname="%s"} %d\n' % (
            egname.replace("'", ""),
            broker_name,
            app_name.replace("'", "").replace(",", ""),
            message_flow_name.replace("'", ""),
            STATUS_MAP[status]
            )
        msg_flow_metric_data += msg_flow_metric
    return msg_flow_metric_data


def main():
    start_time = time.time()
    logger.info("Starting metrics collecting for Integration Bus!")
    try:
        brokers_data = run_iib_command(task='get_brokers_status')
        brokers = get_brokers_status(brokers_data)
        for broker in brokers:
            broker_name, status, qm_name = broker
            broker_data = format_broker(broker_name, status, qm_name)
            if status == 'running.':
                broker_row_data = run_iib_command(
                    task='get_broker_objects',
                    broker_name=broker_name
                    )
                exec_groups, applications, message_flows = get_broker_items(broker_row_data)
                exec_groups_data = format_exec_groups(exec_groups)
                applications_data = format_applications(applications, broker_name)
                message_flows_data = format_message_flows(message_flows, broker_name)
                metric_data = "{0}{1}{2}{3}".format(
                    broker_data,
                    exec_groups_data,
                    applications_data,
                    message_flows_data
                    )
                put_metric_to_gateway(metric_data, broker_name)
                logger.info("All metrics pushed successfully!")
            else:
                logger.warning("The status of broker is {0}\nOther metrics will not be collected!".format(status))
                put_metric_to_gateway(broker_data, broker_name)
    except PrometheusBadResponse as error:
        logger.error(error)
    except Exception as e:
        tb = sys.exc_info()[-1]
        stk = traceback.extract_tb(tb, 1)[0]
        logger.error("Function: {0}\n{1}".format(stk, e))
    logger.info("Script finished in - %s seconds -" % (time.time() - start_time))


if __name__ == "__main__":
    while True:
        main()
        time.sleep(60)

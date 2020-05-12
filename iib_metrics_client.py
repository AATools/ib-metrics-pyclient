# -*- coding: utf-8 -*-
"""Python client for collecting IBM Integration Bus metrics and exporting to Prometheus pushgateway."""
import sys
import time
import traceback
import platform
import requests
from requests import ConnectionError
from urllib3.exceptions import ResponseError
from modules.iib_brokers import (
    get_brokers_status,
    format_broker,
    get_broker_items)
from modules.iib_exec_groups import format_exec_groups
from modules.iib_applications import format_applications
from modules.iib_message_flows import format_message_flows
from log.logger_client import set_logger
from modules.iib_api import run_iib_command


logger = set_logger()


class PrometheusBadResponse(Exception):
    pass


def static_content():
    """Client name and version."""
    name = "ib-metrics-pyclient"
    version = "0.2"
    return '{0} v.{1}'.format(name, version)


def put_metric_to_gateway(metric_data, job):
    """Sends data to Prometheus pushgateway."""
    hostname = platform.node()
    port = 9091
    src_url = "http://{0}:{1}".format(hostname, port)
    headers = {"Content-Type": "text/plain; version=0.0.4"}
    dest_url = "{0}/metrics/job/{1}".format(src_url, job)
    logger.info("Destination url: {0}".format(dest_url))
    # Debug info
    # logger.info("Metric data to push: {0}".format(metric_data))
    try:
        response = requests.put(dest_url, data=metric_data, headers=headers)
        if not response.ok:
            raise PrometheusBadResponse("Bad response - {0} from {1}\nResponseText: {2}".format(response, dest_url, response.text))
        logger.info("Success! Server response: {0}".format(response))
    except (ConnectionError, ResponseError):
        raise PrometheusBadResponse("{0} is not available!".format(dest_url))


def main():
    start_time = time.time()
    logger.info("Starting metrics collecting for Integration Bus!")
    try:
        brokers_data = run_iib_command(task='get_brokers_status')
        brokers = get_brokers_status(brokers_data=brokers_data)
        for broker in brokers:
            broker_name, status, qm_name = broker
            broker_data = format_broker(
                broker_name=broker_name,
                status=status,
                qm_name=qm_name)
            if status == 'running.':
                broker_row_data = run_iib_command(
                    task='get_broker_objects',
                    broker_name=broker_name)
                exec_groups, applications, message_flows = get_broker_items(broker_row_data=broker_row_data)
                exec_groups_data = format_exec_groups(exec_groups=exec_groups)
                applications_data = format_applications(applications=applications, broker_name=broker_name)
                message_flows_data = format_message_flows(message_flows=message_flows, broker_name=broker_name)
                metric_data = "{0}{1}{2}{3}".format(
                    broker_data,
                    exec_groups_data,
                    applications_data,
                    message_flows_data)
                put_metric_to_gateway(metric_data=metric_data, job=broker_name)
                logger.info("All metrics pushed successfully!")
            else:
                logger.warning("The status of broker is {0}\nOther metrics will not be collected!".format(status))
                put_metric_to_gateway(metric_data=metric_data, job=broker_name)
        logger.info("Script finished in - {0} seconds -".format(time.time() - start_time))
    except PrometheusBadResponse as error:
        logger.error(error)
    except Exception as e:
        tb = sys.exc_info()[-1]
        stk = traceback.extract_tb(tb, 1)[0]
        logger.error("Function: {0}\n{1}".format(stk, e))


if __name__ == "__main__":
    logger.info("Run {0}".format(static_content()))
    while True:
        main()
        time.sleep(60)

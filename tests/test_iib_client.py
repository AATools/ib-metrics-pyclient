# -*- coding: utf-8 -*-
import os
import sys
import unittest
from iib_metrics_client import (
    get_brokers_status,
    get_broker_items,
    format_broker,
    format_exec_groups,
    format_applications,
    format_message_flows,
    STATUS_MAP,
    )
sys.path.append(os.getcwd())


class TestGetBrokersStatus(unittest.TestCase):
    def test_get_brokers_status(self):
        input_data = "BIP1284I: Broker 'TEST' on queue manager 'TEST' is running. \n"
        check_data = [['TEST', 'running.', 'TEST']]
        self.assertEqual(check_data, get_brokers_status(input_data))


class TestGetBrokerItems(unittest.TestCase):
    def test_get_broker_items(self):
        input_data = '''"-----------------------------------
BIP1286I: Execution group 'IB' on broker 'TEST' is running. 
BIP1287I: Execution group 'IB' on broker 'TEST2' is stopped. 
BIP1275I: Application 'Adapter' on execution group 'IB' is running. 
BIP1276I: Application 'Adapter2' on execution group 'IB' is stopped. 
BIP1277I: Message flow 'esb.adapter.RequestForESB' on execution group 'IB' is running. (Application 'Adapter', Library '') 
BIP1278I: Message flow 'esb.adapter.RequestForESB2' on execution group 'IB' is stopped. (Application 'Adapter', Library '') 
BIP1274I: Library 'Utils' is deployed to execution group 'IB'. (Application 'Adapter') 
BIP1299I: File 'esb.util.subflow' is deployed to execution group 'IB'. (Application 'Adapter', Library 'Utils') 
BIP8071I: Successful command completion.\n"'''
        check_data = (["BIP1286I: Execution group 'IB' on broker 'TEST' is running. ",
                       "BIP1287I: Execution group 'IB' on broker 'TEST2' is stopped. "],
                      ["BIP1275I: Application 'Adapter' on execution group 'IB' is running. ",
                       "BIP1276I: Application 'Adapter2' on execution group 'IB' is stopped. "],
                      ["BIP1277I: Message flow 'esb.adapter.RequestForESB' on execution group 'IB' is running. (Application 'Adapter', Library '') ",
                       "BIP1278I: Message flow 'esb.adapter.RequestForESB2' on execution group 'IB' is stopped. (Application 'Adapter', Library '') "])
        self.assertEqual(check_data, get_broker_items(input_data))


class TestFormatBroker(unittest.TestCase):
    input_data_broker = 'TEST'
    input_data_qmname = 'TEST'

    def test_format_broker_good_status(self):
        for status in STATUS_MAP:
            check_data = 'ib_broker_status{brokername="%s", qmname="%s"} %s\n' % (self.input_data_broker, self.input_data_qmname, STATUS_MAP[status])
            self.assertEqual(check_data, format_broker(self.input_data_broker, status, self.input_data_qmname))

    def test_format_broker_bad_status(self):
        status = 'test.'
        self.assertRaises(KeyError, format_broker, self.input_data_broker, status, self.input_data_qmname)


class TestFormatApplications(unittest.TestCase):
    input_data_broker = 'TEST'

    def test_format_applications_good_status(self):
        input_data_app = ["BIP1275I: Application 'TEST.RUNNING' on execution group 'TEST' is running. ",
                          "BIP1276I: Application 'TEST.STOPPED' on execution group 'TEST' is stopped. "]
        check_data = '''ib_application_status{egname="TEST", brokername="TEST", appname="TEST.RUNNING"} 1
ib_application_status{egname="TEST", brokername="TEST", appname="TEST.STOPPED"} 0\n'''
        self.assertEqual(check_data, format_applications(input_data_app, self.input_data_broker))

    def test_format_applications_bas_status(self):
        input_data_app = ["BIP1111I: Execution group 'TEST.INVALID' on execution group 'TEST' is invalid. "]
        self.assertRaises(KeyError, format_applications, input_data_app, self.input_data_broker)


class TestFormatExecGroups(unittest.TestCase):
    def test_format_exec_group_good_status(self):
        input_data_eg = ["BIP1286I: Execution group 'TEST.RUNNING' on broker 'TEST' is running. ",
                         "BIP1287I: Execution group 'TEST.STOPPED' on broker 'TEST' is stopped. "]
        check_data = '''ib_exec_group_status{brokername="TEST", egname="TEST.RUNNING"} 1
ib_exec_group_status{brokername="TEST", egname="TEST.STOPPED"} 0\n'''
        self.assertEqual(check_data, format_exec_groups(input_data_eg))

    def test_format_exec_group_bad_status(self):
        input_data_eg = ["BIP1111I: Execution group 'TEST.INVALID' on broker 'TEST' is invalid. "]
        self.assertRaises(KeyError, format_exec_groups, input_data_eg)


class TestFormatMessageFlows(unittest.TestCase):
    input_data_broker = 'TEST'

    def test_fformat_message_flows_good_status(self):
        input_data_msgflow = ["BIP1277I: Message flow 'TEST.RUNNING' on execution group 'TEST' is running. (Application 'TEST', Library '') ",
                            "BIP1278I: Message flow 'TEST.STOPPED' on execution group 'TEST' is stopped. (Application 'TEST', Library '') "]
        check_data = '''ib_message_flow_status{egname="TEST", brokername="TEST", appname="TEST", messageflowname="TEST.RUNNING"} 1
ib_message_flow_status{egname="TEST", brokername="TEST", appname="TEST", messageflowname="TEST.STOPPED"} 0\n'''
        self.assertEqual(check_data, format_message_flows(input_data_msgflow, self.input_data_broker))

    def test_format_message_flows_bad_status(self):
        input_data_msgflow = ["BIP1111I: Message flow 'TETS.INVALID' on execution group 'TEST' is invalid. (Application 'TEST', Library '') "]
        self.assertRaises(KeyError, format_message_flows, input_data_msgflow, self.input_data_broker)


if __name__ == '__main__':
    unittest.main()

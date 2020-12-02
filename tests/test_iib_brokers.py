# -*- coding: utf-8 -*-
"""Tests for `iib_brokers`."""
import unittest
from modules.iib_brokers import (
    get_brokers_status,
    get_broker_items,
    format_broker,
    get_metric_name,
    get_metric_annotation)
from modules.iib_api import get_platform_params_for_commands


class TestGetBrokersStatus(unittest.TestCase):
    def test_get_brokers_status(self):
        """Test for `get_brokers_status` function."""
        input_data = """\
BIP1284I: Broker 'TEST' on queue manager 'QM1' is running.
BIP1285I: Broker 'TEST' on queue manager 'QM1' is stopped.
BIP1293I: Broker 'TEST' is a multi-instance broker running in standby mode on queue manager 'QM1'.
BIP1294I: Broker 'TEST' is a multi-instance broker running in standby mode on queue manager 'QM1'.\nMore information will be available when the broker instance is active.
BIP1295I: Broker 'TEST' is an active multi-instance or High Availability broker that is running on queue manager 'QM1'.
BIP1296I: Broker 'TEST' is stopped. It is a multi-instance broker and will be started as a WebSphere MQ service by queue manager 'QM1'.
BIP1297I: Broker 'TEST' is a multi-instance broker running in standby mode on queue manager 'QM1'.
BIP1298I: Broker 'TEST' is stopped. It will be started as a WebSphere MQ service by queue manager 'QM1'.
"""
        check_data = [
            ['TEST', 'running', 'QM1'],
            ['TEST', 'stopped', 'QM1'],
            ['TEST', 'running', 'QM1'],
            ['TEST', 'running', 'QM1'],
            ['TEST', 'running', 'QM1'],
            ['TEST', 'stopped', 'QM1'],
            ['TEST', 'running', 'QM1'],
            ['TEST', 'stopped', 'QM1']]
        bip_codes_brokers = get_platform_params_for_commands (iib_ver='9')[1]
        self.assertEqual(check_data, get_brokers_status(brokers_data=input_data, bip_codes=bip_codes_brokers))

    def test_get_integration_nodes_status(self):
        """Test for `get_brokers_status` function for Integration Bus v10."""
        input_data = """\
BIP1284I: Integration node 'TEST' with default queue manager 'QM1 and administration URI 'http://testhost:4415' is running.
BIP1285I: Integration node 'TEST' on queue manager 'QM1' is stopped.
BIP1295I: Integration node 'TEST' is an active multi-instance or High Availability integration node that is running on queue manager 'QM1'.
BIP1296I: Integration node 'TEST' is stopped. It is a multi-instance integration node and will be started as a WebSphere MQ service by queue manager 'QM1'.
BIP1298I: Integration node 'TEST' is stopped. It will be started as a WebSphere MQ service by queue manager 'QM1'.
BIP1325I: Integration node 'TEST' with administration URI 'http://testhost:4415' is running.
BIP1326I: Integration node 'TEST' is stopped.
BIP1340I: Integration node 'TEST' is running.
BIP1353I: Integration node 'TEST' with default queue manager 'QM1' is running.
BIP1366I: Integration node 'TEST' is an active multi-instance or High Availability integration node that is running on queue manager 'QM1'. The administration URI is 'http://testhost:4415'
BIP1376I: Integration node 'TEST' is an active multi-instance or High Availability integration node that is running on queue manager 'QM1'. The administration URI is 'http://testhost:4415'
BIP1377I: Integration node 'TEST' is stopped. It is a multi-instance integration node and will be started as a WebSphere MQ service by queue manager 'QM1'. Web administration will be enabled when the node is active.\n\
"""
        check_data = [
            ['TEST', 'running', 'QM1'],
            ['TEST', 'stopped', 'QM1'],
            ['TEST', 'running', 'QM1'],
            ['TEST', 'stopped', 'QM1'],
            ['TEST', 'stopped', 'QM1'],
            ['TEST', 'running', ''],
            ['TEST', 'stopped', ''],
            ['TEST', 'running', ''],
            ['TEST', 'running', 'QM1'],
            ['TEST', 'running', 'QM1'],
            ['TEST', 'running', 'QM1'],
            ['TEST', 'stopped', 'QM1']]
        bip_codes_integration_nodes = get_platform_params_for_commands (iib_ver='10')[1]
        self.assertEqual(check_data, get_brokers_status(brokers_data=input_data, bip_codes=bip_codes_integration_nodes))


class TestGetBrokerItems(unittest.TestCase):
    def test_get_broker_items(self):
        """Test for `get_broker_items` function."""
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
        check_data = (["BIP1286I: Execution group 'IB' on broker 'TEST' is running.",
                       "BIP1287I: Execution group 'IB' on broker 'TEST2' is stopped."],
                      ["BIP1275I: Application 'Adapter' on execution group 'IB' is running.",
                       "BIP1276I: Application 'Adapter2' on execution group 'IB' is stopped."],
                      ["BIP1277I: Message flow 'esb.adapter.RequestForESB' on execution group 'IB' is running. (Application 'Adapter', Library '')",
                       "BIP1278I: Message flow 'esb.adapter.RequestForESB2' on execution group 'IB' is stopped. (Application 'Adapter', Library '')"])
        self.assertEqual(check_data, get_broker_items(broker_row_data=input_data))


class TestFormatBroker(unittest.TestCase):
    input_data_broker = 'TEST'
    input_data_qmname = 'TEST'

    def test_format_broker_good_status(self):
        """Test for `format_broker` function for good case."""
        check_data = '''\
# HELP ib_broker_status Current status of IB broker.
# TYPE ib_broker_status gauge
ib_broker_status{{brokername="{0}", qmname="{1}"}} {2}\n\
'''.format(self.input_data_broker,
           self.input_data_qmname,
           1)
        self.assertEqual(
            check_data,
            format_broker(
                broker_name=self.input_data_broker,
                status='running',
                qm_name=self.input_data_qmname))

    def test_format_broker_bad_status(self):
        """Test for `format_broker` function for bad case."""
        self.assertRaises(
            KeyError,
            format_broker,
            broker_name=self.input_data_broker,
            status='test.',
            qm_name=self.input_data_qmname)


class GetMetricAnnotation(unittest.TestCase):
    def test_get_metric_name(self):
        """Test for `get_metric_name` function."""
        self.assertEqual('ib_broker_status', get_metric_name(metric_label='status'))

    def test_get_metric_annotation(self):
        """Tests for `get_metric_annotation` function."""
        self.assertIsInstance(get_metric_annotation(), dict)
        self.assertIsInstance(get_metric_annotation().get('status'), str)


if __name__ == '__main__':
    unittest.main()

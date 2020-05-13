# -*- coding: utf-8 -*-
"""Tests for `iib_brokers`."""
import unittest
from modules.iib_brokers import (
    get_brokers_status,
    get_broker_items,
    format_broker,
    get_metric_name,
    get_metric_annotation)


class TestGetBrokersStatus(unittest.TestCase):
    def test_get_brokers_status(self):
        """Test for `get_brokers_status` function."""
        input_data = "BIP1284I: Broker 'TEST' on queue manager 'TEST' is running.\n"
        check_data = [['TEST', 'running.', 'TEST']]
        self.assertEqual(check_data, get_brokers_status(brokers_data=input_data))


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
                status='running.',
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

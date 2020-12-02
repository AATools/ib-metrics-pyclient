# -*- coding: utf-8 -*-
"""Tests for `iib_message_flows`."""
import os
import sys
import unittest
from modules.iib_message_flows import (
    format_message_flows,
    get_metric_name,
    get_metric_annotation)
from modules.iib_api import get_platform_params_for_commands
sys.path.append(os.getcwd())


class TestFormatMessageFlows(unittest.TestCase):
    input_data_broker = 'TEST'

    def test_fformat_message_flows_good_status(self):
        """Test for `format_message_flows` function for good case."""
        input_data_msgflow = [
            "BIP1277I: Message flow 'TEST.RUNNING' on execution group 'TEST' is running. (Application 'TEST', Library '')",
            "BIP1278I: Message flow 'TEST.STOPPED' on execution group 'TEST' is stopped. (Application 'TEST', Library '')"]
        check_data = '''\
# HELP ib_message_flow_status Current status of IB message flow.
# TYPE ib_message_flow_status gauge
ib_message_flow_status{egname="TEST", brokername="TEST", appname="TEST", messageflowname="TEST.RUNNING"} 1
ib_message_flow_status{egname="TEST", brokername="TEST", appname="TEST", messageflowname="TEST.STOPPED"} 0\n'''
        bip_codes_components = get_platform_params_for_commands(iib_ver='9')[2]
        self.assertEqual(
            check_data,
            format_message_flows(
                message_flows=input_data_msgflow,
                broker_name=self.input_data_broker,
                bip_codes=bip_codes_components))
        bip_codes_components = get_platform_params_for_commands(iib_ver='10')[2]
        self.assertEqual(
            check_data,
            format_message_flows(
                message_flows=input_data_msgflow,
                broker_name=self.input_data_broker,
                bip_codes=bip_codes_components))

    def test_format_message_flows_bad_status(self):
        """Test for `format_message_flows` function for bad case."""
        input_data_msgflow = [
            "BIP1111I: Message flow 'TETS.INVALID' on execution group 'TEST' is invalid. (Application 'TEST', Library '')"]
        check_data = ''
        bip_codes_components = get_platform_params_for_commands(iib_ver='9')[2]
        self.assertEqual(
            check_data,
            format_message_flows(
                message_flows=input_data_msgflow,
                broker_name=self.input_data_broker,
                bip_codes=bip_codes_components))
        bip_codes_components = get_platform_params_for_commands(iib_ver='10')[2]
        self.assertEqual(
            check_data,
            format_message_flows(
                message_flows=input_data_msgflow,
                broker_name=self.input_data_broker,
                bip_codes=bip_codes_components))


class GetMetricAnnotation(unittest.TestCase):
    def test_get_metric_name(self):
        """Test for `get_metric_name` function."""
        self.assertEqual('ib_message_flow_status', get_metric_name(metric_label='status'))

    def test_get_metric_annotation(self):
        """Tests for `get_metric_annotation` function."""
        self.assertIsInstance(get_metric_annotation(), dict)
        self.assertIsInstance(get_metric_annotation().get('status'), str)


if __name__ == '__main__':
    unittest.main()

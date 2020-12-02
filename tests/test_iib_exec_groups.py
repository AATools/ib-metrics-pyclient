# -*- coding: utf-8 -*-
"""Tests for `iib_exec_groups`."""
import os
import sys
import unittest
from modules.iib_exec_groups import (
    format_exec_groups,
    get_metric_name,
    get_metric_annotation)
from modules.iib_api import get_platform_params_for_commands
sys.path.append(os.getcwd())


class TestFormatExecGroups(unittest.TestCase):

    def test_format_exec_group_good_status(self):
        """Test for `format_exec_groups` function for good case."""
        input_data_eg = ["BIP1286I: Execution group 'TEST.RUNNING' on broker 'TEST' is running.",
                         "BIP1287I: Execution group 'TEST.STOPPED' on broker 'TEST' is stopped."]
        check_data = '''\
# HELP ib_exec_group_status Current status of IB execution group.
# TYPE ib_exec_group_status gauge
ib_exec_group_status{brokername="TEST", egname="TEST.RUNNING"} 1
ib_exec_group_status{brokername="TEST", egname="TEST.STOPPED"} 0\n'''
        bip_codes_components = get_platform_params_for_commands(iib_ver='9')[2]
        self.assertEqual(
            check_data,
            format_exec_groups(
                exec_groups=input_data_eg,
                bip_codes=bip_codes_components))
        bip_codes_components = get_platform_params_for_commands(iib_ver='10')[2]
        input_data_eg = ["BIP1286I: Integration server 'TEST.RUNNING' on integration node 'TEST' is running.",
                         "BIP1287I: Integration server 'TEST.STOPPED' on integration node 'TEST' is stopped."]
        self.assertEqual(
            check_data,
            format_exec_groups(
                exec_groups=input_data_eg,
                bip_codes=bip_codes_components))

    def test_format_exec_group_bad_status(self):
        """Test for `format_exec_groups` function for good case."""
        check_data = ''
        input_data_eg = ["BIP1111I: Execution group 'TEST.INVALID' on broker 'TEST' is invalid."]
        bip_codes_components = get_platform_params_for_commands(iib_ver='9')[2]
        self.assertEqual(
            check_data,
            format_exec_groups(
                exec_groups=input_data_eg,
                bip_codes=bip_codes_components))
        input_data_eg = ["BIP1111I: Integration server 'TEST.INVALID' on integration node 'TEST' is invalid."]
        bip_codes_components = get_platform_params_for_commands(iib_ver='10')[2]
        self.assertEqual(
            check_data,
            format_exec_groups(
                exec_groups=input_data_eg,
                bip_codes=bip_codes_components))


class GetMetricAnnotation(unittest.TestCase):
    def test_get_metric_name(self):
        """Test for `get_metric_name` function."""
        self.assertEqual('ib_exec_group_status', get_metric_name(metric_label='status'))

    def test_get_metric_annotation(self):
        """Tests for `get_metric_annotation` function."""
        self.assertIsInstance(get_metric_annotation(), dict)
        self.assertIsInstance(get_metric_annotation().get('status'), str)


if __name__ == '__main__':
    unittest.main()

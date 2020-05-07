# -*- coding: utf-8 -*-
"""Tests for `iib_applications`."""
import os
import sys
import unittest
from modules.iib_applications import (
    format_applications,
    get_metric_name,
    get_metric_annotation)
sys.path.append(os.getcwd())


class TestFormatApplications(unittest.TestCase):
    input_data_broker = 'TEST'

    def test_format_applications_good_status(self):
        """Test for `format_applications` function for good case."""
        input_data_app = [
            "BIP1275I: Application 'TEST.RUNNING' on execution group 'TEST' is running.",
            "BIP1276I: Application 'TEST.STOPPED' on execution group 'TEST' is stopped."]
        check_data = '''\
# HELP ib_application_status Current status of IB application.
# TYPE ib_application_status gauge
ib_application_status{egname="TEST", brokername="TEST", appname="TEST.RUNNING"} 1
ib_application_status{egname="TEST", brokername="TEST", appname="TEST.STOPPED"} 0\n'''
        self.assertEqual(
            check_data,
            format_applications(
                applications=input_data_app,
                broker_name=self.input_data_broker))

    def test_format_applications_bad_status(self):
        """Test for `format_applications` function for bad case."""
        input_data_app = ["BIP1111I: Execution group 'TEST.INVALID' on execution group 'TEST' is invalid."]
        self.assertRaises(
            KeyError,
            format_applications,
            applications=input_data_app,
            broker_name=self.input_data_broker)


class GetMetricAnnotation(unittest.TestCase):
    def test_get_metric_name(self):
        """Test for `get_metric_name` function."""
        self.assertEqual('ib_application_status', get_metric_name(metric_label='status'))

    def test_get_metric_annotation(self):
        """Tests for `get_metric_annotation` function."""
        self.assertIsInstance(get_metric_annotation(), dict)
        self.assertIsInstance(get_metric_annotation().get('status'), str)


if __name__ == '__main__':
    unittest.main()

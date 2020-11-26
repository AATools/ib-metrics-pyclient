# -*- coding: utf-8 -*-
"""Tests for `iib_metrics_client`."""
import os
import sys
import unittest
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
from iib_metrics_client import (
    get_iib_metrics,
    put_metric_to_gateway,
    static_content,
    PrometheusBadResponse)
sys.path.append(os.getcwd())


class MockFunction():
    @staticmethod
    def mock_logging_info(msg):
        """Mock for `logger.info` function."""
        pass

    @staticmethod
    def mock_run_iib_command(**kwargs):
        """Mock for `run_iib_command` function."""
        return 'OK'

    @staticmethod
    def mock_put_metric_to_gateway(metric_data, job):
        """Mock for `put_metric_to_gateway` function."""
        pass


class TestGetIIBMetrics(unittest.TestCase):
    pushgateway_host = 'testhost'
    pushgateway_port = '9091'
    iib_ver = '9'

    Mocked = MockFunction()
    @patch('iib_metrics_client.logger.info', side_effect=Mocked.mock_logging_info)
    @patch('iib_metrics_client.run_iib_command', side_effect=Mocked.mock_run_iib_command)
    @patch('iib_metrics_client.put_metric_to_gateway', side_efgect=Mocked.mock_put_metric_to_gateway)
    def test_get_iib_metrics(
            self,
            mock_logging_info,
            mock_run_iib_command,
            mock_put_metric_to_gateway):
        """Tests for `get_iib_metrics` function."""
        with patch('iib_metrics_client.get_brokers_status') as mock_get_brokers_status:
            mock_get_brokers_status.return_value = [['TEST', 'running.', 'TEST']]
            self.assertEqual(
                get_iib_metrics(
                    pushgateway_host=self.pushgateway_host,
                    pushgateway_port=self.pushgateway_port,
                    iib_ver=self.iib_ver),
                None)
            mock_get_brokers_status.return_value = [['TEST', 'stopped.', 'TEST']]
            self.assertEqual(
                get_iib_metrics(
                    pushgateway_host=self.pushgateway_host,
                    pushgateway_port=self.pushgateway_port,
                    iib_ver=self.iib_ver),
                None)

    @patch('iib_metrics_client.logger.info', side_effect=Mocked.mock_logging_info)
    @patch('iib_metrics_client.logger.error', side_effect=Exception())
    def test_get_iib_metrics_exception(self, mock_logging_info, mock_logging_error):
        """Test for `get_iib_metrics` function for exceptions."""
        with patch('iib_metrics_client.run_iib_command') as mock_iib_command:
            mock_iib_command.side_effect = PrometheusBadResponse
            self.assertRaises(
                Exception,
                get_iib_metrics,
                pushgateway_host=self.pushgateway_host,
                pushgateway_port=self.pushgateway_port,
                iib_ver=self.iib_ver)
            mock_iib_command.side_effect = Exception()
            self.assertRaises(
                Exception,
                get_iib_metrics,
                pushgateway_host=self.pushgateway_host,
                pushgateway_port=self.pushgateway_port,
                iib_ver=self.iib_ver)


class TestPutMetricToGateway(unittest.TestCase):
    metric_data=''
    job='TEST'
    pushgateway_host = 'testhost'
    pushgateway_port = '9091'

    Mocked = MockFunction()
    @patch('iib_metrics_client.logger.info', side_effect=Mocked.mock_logging_info)
    def test_put_metric_to_gateway(self, mock_logging_info):
        """Tests for `put_metric_to_gateway` function."""
        with patch('iib_metrics_client.requests.put') as mock_request:
            mock_request.return_value.ok = True
            self.assertEqual(
                put_metric_to_gateway(
                    metric_data=self.metric_data,
                    job=self.job,
                    pushgateway_host=self.pushgateway_host,
                    pushgateway_port=self.pushgateway_port),
                None)
            mock_request.return_value.ok = False
            self.assertRaises(
                PrometheusBadResponse,
                put_metric_to_gateway,
                metric_data=self.metric_data,
                job=self.job,
                pushgateway_host=self.pushgateway_host,
                pushgateway_port=self.pushgateway_port)

    @patch('iib_metrics_client.logger.info', side_effect=Mocked.mock_logging_info)
    def test_put_metric_to_gateway_except(self,  mock_logging_info):
        """Test for `put_metric_to_gateway` function for `ConnectionError` exceptions."""
        self.assertRaises(
            PrometheusBadResponse,
            put_metric_to_gateway,
            metric_data=self.metric_data,
            job=self.job,
            pushgateway_host=self.pushgateway_host,
            pushgateway_port=self.pushgateway_port)


class TestStaticContent(unittest.TestCase):
    def test_static_content(self):
        """Test for `static_content` function."""
        self.assertIsInstance(static_content(), str)


if __name__ == '__main__':
    unittest.main()

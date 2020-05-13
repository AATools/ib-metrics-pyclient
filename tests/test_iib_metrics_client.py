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
    main,
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


class TestMain(unittest.TestCase):
    Mocked = MockFunction()
    @patch('iib_metrics_client.logger.info', side_effect=Mocked.mock_logging_info)
    @patch('iib_metrics_client.run_iib_command', side_effect=Mocked.mock_run_iib_command)
    @patch('iib_metrics_client.put_metric_to_gateway', side_efgect=Mocked.mock_put_metric_to_gateway)
    def test_main(self,
                  mock_logging_info,
                  mock_run_iib_command,
                  mock_put_metric_to_gateway):
        """Tests for `main` function."""
        with patch('iib_metrics_client.get_brokers_status') as mock_get_brokers_status:
            mock_get_brokers_status.return_value = [['TEST', 'running.', 'TEST']]
            self.assertEqual(main(), None)
            mock_get_brokers_status.return_value = [['TEST', 'stopped.', 'TEST']]
            self.assertEqual(main(), None)

    @patch('iib_metrics_client.logger.info', side_effect=Mocked.mock_logging_info)
    @patch('iib_metrics_client.logger.error', side_effect=Exception())
    def test_main_exception(self, mock_logging_info, mock_logging_error):
        """Test for `main` function for exceptions."""
        with patch('iib_metrics_client.run_iib_command') as mock_iib_command:
            mock_iib_command.side_effect = PrometheusBadResponse
            self.assertRaises(Exception, main)
            mock_iib_command.side_effect = Exception()
            self.assertRaises(Exception, main)


class TestPutMetricToGateway(unittest.TestCase):
    Mocked = MockFunction()
    @patch('iib_metrics_client.logger.info', side_effect=Mocked.mock_logging_info)
    def test_put_metric_to_gateway(self, mock_logging_info):
        """Tests for `put_metric_to_gateway` function."""
        with patch('iib_metrics_client.requests.put') as mock_request:
            mock_request.return_value.ok = True
            self.assertEqual(put_metric_to_gateway(metric_data='', job='TEST'), None)
            mock_request.return_value.ok = False
            self.assertRaises(PrometheusBadResponse, put_metric_to_gateway, metric_data='', job='TEST')

    @patch('iib_metrics_client.logger.info', side_effect=Mocked.mock_logging_info)
    def test_put_metric_to_gateway_except(self,  mock_logging_info):
        """Test for `put_metric_to_gateway` function for `ConnectionError` exceptions."""
        self.assertRaises(PrometheusBadResponse, put_metric_to_gateway, metric_data='', job='TEST')


class TestStaticContent(unittest.TestCase):
    def test_static_content(self):
        """Test for `static_content` function."""
        self.assertIsInstance(static_content(), str)


if __name__ == '__main__':
    unittest.main()

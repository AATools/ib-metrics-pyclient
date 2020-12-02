# -*- coding: utf-8 -*-
"""Tests for `iib_metrics_client`."""
import os
import sys
import unittest
import argparse
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
from iib_metrics_client import (
    get_iib_metrics,
    put_metric_to_gateway,
    static_content,
    get_version_from_env,
    parse_commandline_args,
    PrometheusBadResponse)
from modules.iib_api import get_platform_params_for_commands
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
    mqsilist_command = str()
    bip_codes_brokers = dict()
    bip_codes_components = dict()

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
            mock_get_brokers_status.return_value = [['TEST', 'running', 'TEST']]
            self.assertEqual(
                get_iib_metrics(
                    pushgateway_host=self.pushgateway_host,
                    pushgateway_port=self.pushgateway_port,
                    mqsilist_command=self.mqsilist_command,
                    bip_codes_brokers=self.bip_codes_brokers,
                    bip_codes_components= self.bip_codes_components),
                None)
            mock_get_brokers_status.return_value = [['TEST', 'stopped', 'TEST']]
            self.assertEqual(
                get_iib_metrics(
                    pushgateway_host=self.pushgateway_host,
                    pushgateway_port=self.pushgateway_port,
                    mqsilist_command=self.mqsilist_command,
                    bip_codes_brokers=self.bip_codes_brokers,
                    bip_codes_components= self.bip_codes_components),
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
                mqsilist_command=self.mqsilist_command,
                bip_codes_brokers=self.bip_codes_brokers,
                bip_codes_components= self.bip_codes_components)
            mock_iib_command.side_effect = Exception()
            self.assertRaises(
                Exception,
                get_iib_metrics,
                pushgateway_host=self.pushgateway_host,
                pushgateway_port=self.pushgateway_port,
                mqsilist_command=self.mqsilist_command,
                bip_codes_brokers=self.bip_codes_brokers,
                bip_codes_components= self.bip_codes_components)


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


class TestGetVersionFromEnv(unittest.TestCase):
    Mocked = MockFunction()
    @patch.dict(os.environ, {"MQSI_VERSION_V": "10"})
    @patch('iib_metrics_client.logger.info', side_effect=Mocked.mock_logging_info)
    def test_get_version_from_env_exist(self, mock_logging_info):
        """Test for `get_version_from_env` function for exist `MQSI_VERSION_V` variable."""
        self.assertEqual(get_version_from_env(), "10")

    @patch('iib_metrics_client.logger.info', side_effect=Mocked.mock_logging_info)
    def test_get_version_from_env_not_exist(self, mock_logging_info):
        """Test for `get_version_from_env` function for not exist `MQSI_VERSION_V` variable."""
        self.assertEqual(get_version_from_env(), "9")


class TestParseCommandlineArgs(unittest.TestCase):
    pushgateway_host = 'testhost'
    pushgateway_port = '9091'
    iib_ver = '9'

    Mocked = MockFunction()
    @patch('iib_metrics_client.logger.info', side_effect=Mocked.mock_logging_info)
    @patch(
        'argparse.ArgumentParser.parse_args',
        return_value=argparse.Namespace(
            pushgateway_host= pushgateway_host,
            pushgateway_port= pushgateway_port,
            iib_cmd_ver= iib_ver))
    def test_parse_commandline_args(self, mock_logging_info, mock_args):
        """Test for `parse_commandline_args` function."""
        self.assertEqual(
            parse_commandline_args(), 
            (self.pushgateway_host, self.pushgateway_port, self.iib_ver))

    @patch('iib_metrics_client.logger.info', side_effect=Mocked.mock_logging_info)
    @patch(
        'argparse.ArgumentParser.parse_args', 
        return_value=argparse.Namespace(
            pushgateway_host= pushgateway_host,
            pushgateway_port= pushgateway_port,
            iib_cmd_ver=None))
    def test_parse_commandline_args_is_none(self, mock_logging_info, mock_args):
        """Test for `parse_commandline_args` function for `iib_cmd_ver` is None."""
        self.assertEqual(
            parse_commandline_args(),
            (self.pushgateway_host, self.pushgateway_port, self.iib_ver))

    @patch('iib_metrics_client.logger.info', side_effect=Mocked.mock_logging_info)
    @patch(
        'argparse.ArgumentParser.parse_args', 
        return_value=argparse.Namespace(
            pushgateway_host= pushgateway_host,
            pushgateway_port= pushgateway_port,
            iib_cmd_ver='42'))
    def test_parse_commandline_args_is_42(self, mock_logging_info, mock_args):
        """Test for `parse_commandline_args` function for `iib_cmd_ver` is None."""
        self.assertEqual(
            parse_commandline_args(),
            (self.pushgateway_host, self.pushgateway_port, self.iib_ver))



if __name__ == '__main__':
    unittest.main()

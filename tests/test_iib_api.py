# -*- coding: utf-8 -*-
"""Tests for `iib_api`."""
import os
import sys
import unittest
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
from modules.iib_api import (
    run_iib_command,
    get_status)
sys.path.append(os.getcwd())


def mock_execute_command(command):
    """Mock for `execute_command` function."""
    return command


class TestRunMqCommand(unittest.TestCase):
    @patch('modules.iib_api.execute_command', side_effect=mock_execute_command)
    def test_run_iib_command(self, execute_command):
        """Tests for `run_iib_command` function."""
        self.assertEqual(
            run_iib_command(task='get_brokers_status'),
            'mqsilist | grep Broker')
        self.assertEqual(
            run_iib_command(task='get_broker_objects', broker_name='TEST'),
            'mqsilist TEST -r')


class TestGetStatus(unittest.TestCase):
    def test_get_status(self):
        """Test for `get_status` function."""
        self.assertEqual(0, get_status(status='stopped'))
        self.assertEqual(1, get_status(status='running'))

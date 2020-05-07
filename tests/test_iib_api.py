# -*- coding: utf-8 -*-
"""Tests for `iib_api`."""
import os
import sys
import unittest
from modules.iib_api import get_status
sys.path.append(os.getcwd())


class TestGetStatus(unittest.TestCase):
    def test_get_status(self):
        """Test for `get_status` function."""
        self.assertEqual(0, get_status(status='stopped.'))
        self.assertEqual(1, get_status(status='running.'))

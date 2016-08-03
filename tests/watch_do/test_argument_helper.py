import unittest
from unittest.mock import patch
import argparse

from watch_do.argument_helper import (
    string_to_method_class,
    list_methods,
    string_to_bool
)
import watch_do.methods.hash

class TestArgumentHelper(unittest.TestCase):
    def test_string_to_method_class(self):
        with self.assertRaises(argparse.ArgumentTypeError,
             msg='exception not raised for invalid method type'):
            string_to_method_class('invalid_method_type')

        cls = string_to_method_class('hash')
        self.assertEqual(cls, watch_do.methods.hash.Hash)

    @patch('os.listdir')
    def test_list_methods(self, os_listdir):
        os_listdir.return_value = [
            'hash.py', 'modifiedtime.py', '__pycache__', '.hash.py.swp'
        ]

        methods = list_methods()

        self.assertIn('hash', methods, 'hash not in methods')
        self.assertIn('modifiedtime', methods, 'modifiedtime not in methods')
        self.assertNotIn('__pycache__', methods, '__pycache__ in methods')
        self.assertNotIn('.hash.py.swp', methods, '.hash.py.swp in methods')

    def test_string_to_bool(self):
        self.assertTrue(string_to_bool('True'), 'not recognising True')
        self.assertTrue(string_to_bool('true'), 'not recognising true')
        self.assertTrue(string_to_bool('t'), 'not recognising t')
        self.assertTrue(string_to_bool('yes'), 'not recognising yes')
        self.assertTrue(string_to_bool('y'), 'not recognising y')

        self.assertFalse(string_to_bool('False'), 'not recognising False')
        self.assertFalse(string_to_bool('false'), 'not recognising false')
        self.assertFalse(string_to_bool('f'), 'not recognising f')
        self.assertFalse(string_to_bool('no'), 'not recognising no')
        self.assertFalse(string_to_bool('n'), 'not recognising n')

        with self.assertRaises(argparse.ArgumentTypeError,
             msg='exception not raised for invalid bool'):
            string_to_bool('neither')


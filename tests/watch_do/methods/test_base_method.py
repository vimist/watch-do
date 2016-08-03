import unittest
from unittest.mock import patch

from watch_do.methods.base_method import BaseMethod


class TestBaseMethod(unittest.TestCase):
    @patch('watch_do.methods.base_method.BaseMethod._detect')
    def setUp(self, basemethod_detect):
        basemethod_detect.return_value = 'Initial value'

        self.base_method = BaseMethod('file_name')

    def test_init(self):
        self.assertEqual(self.base_method._file_name, 'file_name')

    def test_file_name(self):
        self.assertEqual(
            self.base_method._file_name, self.base_method.file_name,
            '_file_name and file_name are not the same')

    def test_detect(self):
        with self.assertRaises(
                NotImplementedError,
                msg='_detect not raising NotImplementedError'):
            self.base_method._detect()

    @patch('watch_do.methods.base_method.BaseMethod._detect')
    def test_has_changed(self, basemethod_detect):
        basemethod_detect.return_value = 'Initial value'

        self.assertFalse(
            self.base_method.has_changed(),
            'initial value incorrectly detected as a change')

        basemethod_detect.return_value = 'Changed value'

        self.assertTrue(
            self.base_method.has_changed(),
            'changed value not detected as a change')

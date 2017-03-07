import unittest
from unittest.mock import Mock, patch

from watch_do.methods.mtime import Mtime


class TestMtime(unittest.TestCase):
    @patch('os.stat')
    def setUp(self, os_stat):
        os_stat.return_value = Mock(st_mtime=123.456)

        self.mtime = Mtime('file_name')

    def test_initial_detect(self):
        self.assertEqual(
            self.mtime._detect_value, 123.456, 'invalid _detect_value')

    def test_detect(self):
        with patch('os.stat') as os_stat:
            os_stat.return_value = Mock(st_mtime=456.789)

            self.assertNotEqual(
                self.mtime._detect_value, self.mtime._detect(),
                'content change not detected')

        self.assertFalse(
            self.mtime._detect(), 'non existant file not detected')

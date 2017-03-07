import io
import unittest
from unittest.mock import patch

from watch_do.methods.hash import Hash


class TestHash(unittest.TestCase):
    @patch('builtins.open')
    def setUp(self, builtins_open):
        builtins_open.return_value = io.BytesIO(b'Initial file content')

        self.hash = Hash('file_name')

    def test_initial_detect(self):
        self.assertEqual(
            len(self.hash._detect_value), 16, 'invalid hash length')

    def test_detect(self):
        with patch('builtins.open') as builtins_open:
            builtins_open.return_value = io.BytesIO(b'Changed file content')

            self.assertNotEqual(
                self.hash._detect_value, self.hash._detect(),
                'content change not detected')

        with patch('builtins.open') as builtins_open:
            builtins_open.side_effect = FileNotFoundError()

            self.assertFalse(
                self.hash._detect(), 'non existant file not detected')

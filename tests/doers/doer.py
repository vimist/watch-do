"""Test the base `Doer` class.
"""

from unittest import TestCase

from watch_do.doers import Doer


class TestDoer(TestCase):
    """Test the base `Doer` class.
    """

    def setUp(self):
        """Create an instance of the doer with a simple command.
        """
        self.shell = Doer('/some/random/file')

    def test___init__(self):
        """Check that the properties are being correctly initialised.
        """
        self.assertEqual(self.shell.file_name, '/some/random/file')

    def test__interpolate_file_name(self):
        """Check that the file name gets interpolated into the command.
        """
        self.assertEqual(
            Doer._interpolate_file_name(
                'A %f B \\%f C %f D \\%f E', '/some/file'),
            'A /some/file B %f C /some/file D %f E')

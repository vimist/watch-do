"""Test the base `Doer` class.
"""

from unittest import TestCase

from watch_do.doers import Doer


class FakeDoer(Doer):
    """A fake doer to test with as we can't directly instantiate the
    :class:`.Doer` class.
    """
    def run(self):
        """Get the fixed return value of this fake doer.

        Returns:
            str: Always returns 'Hello' (unless patched)
        """
        return 'Hello'


class TestDoer(TestCase):
    """Test the base `Doer` class.
    """

    def setUp(self):
        """Create an instance of the doer with a simple command.
        """
        self.shell = FakeDoer('shell::echo "%f changed."')

    def test___init__(self):
        """Check that the properties are being correctly initialised.
        """
        self.assertEqual(self.shell.command, 'shell::echo "%f changed."')

    def test__interpolate_file_name(self):
        """Check that the file name gets interpolated into the command.
        """
        self.assertEqual(
            Doer._interpolate_file_name(
                'A %f B \\%f C %f D \\%f E', '/some/file'),
            'A /some/file B %f C /some/file D %f E')

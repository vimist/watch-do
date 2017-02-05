"""Test the `Shell` doer class
"""

from unittest import TestCase

from watch_do.doers import Shell


class TestShell(TestCase):
    """Test the `Shell` doer class
    """

    def setUp(self):
        """Create an instance of the doer with a simple command
        """
        self.shell = Shell('/some/random/file')

    def test__init__(self):
        """Check the properties have been set correctly
        """
        self.assertEqual(self.shell.file_name, '/some/random/file')

    def test_run(self):
        """Check that the `run` method produces the correct output
        """
        self.assertEqual(
            self.shell.run('echo -n "This file changed: %f"'),
            'This file changed: /some/random/file')

        self.assertEqual(
            self.shell.run(
                'echo -n "Hello "; echo -n "World" >&2; echo -n "...";'),
            'Hello World...')

        self.assertEqual(
            self.shell.run('echo -n "Hello"; exit 1'),
            'Hello\nCommand failed to run, exited with error code 1')

"""Test the `Shell` doer class
"""

from unittest import TestCase
from warnings import catch_warnings

from watch_do.doers import Shell


class TestShell(TestCase):
    """Test the `Shell` doer class
    """

    def test__init__(self):
        """Check the properties have been set correctly
        """
        shell = Shell('echo "This file changed: %f"')
        self.assertEqual(shell.command, 'echo "This file changed: %f"')

    def test_run(self):
        """Check that the `run` method produces the correct output
        """
        with catch_warnings(record=True) as warnings:
            shell = Shell('echo -n "Hello"')
            list(shell.run('/some/random/file'))
            self.assertEqual(len(warnings), 0)

        shell = Shell('echo -n "This file changed: %f"')
        self.assertEqual(
            list(shell.run('/some/random/file')),
            ['This file changed: /some/random/file'])

        shell = Shell('echo -n "Hello "; echo -n "World" >&2; echo -n "...";')
        self.assertEqual(
            list(shell.run('')),
            ['Hello World...'])

        shell = Shell('echo -n "Hello"; exit 1')
        self.assertEqual(
            list(shell.run('')),
            ['Hello', 'Command failed to run, exited with error code 1'])

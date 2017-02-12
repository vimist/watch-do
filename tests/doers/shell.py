"""Test the `Shell` doer class
"""

from unittest import TestCase

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
        shell = Shell('echo -n "This file changed: %f"')
        self.assertEqual(
            shell.run('/some/random/file'),
            'This file changed: /some/random/file')

        shell = Shell('echo -n "Hello "; echo -n "World" >&2; echo -n "...";')
        self.assertEqual(
            shell.run(''),
            'Hello World...')

        shell = Shell('echo -n "Hello"; exit 1')
        self.assertEqual(
            shell.run(''),
            'Hello\nCommand failed to run, exited with error code 1')

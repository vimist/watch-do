from unittest import TestCase

from watch_do.doers import Shell
from watch_do import DoerManager


class TestDoerManager(TestCase):
    def setUp(self):
        self.doer_manager = DoerManager(
            ['shell::echo "%f has changed."', 'shell::test', 'echo "Bye"'],
            Shell)

    def test___init__(self):
        """Chack that all passed in parameters have been stored correctly.
        """
        self.assertEqual(
            self.doer_manager.commands,
            ['shell::echo "%f has changed."', 'shell::test', 'echo "Bye"'])

        self.assertEqual(self.doer_manager.default_doer, Shell)

    def test__process_commands(self):
        """Check that the commands have been converted to doers.
        """
        self.assertIsInstance(self.doer_manager.doers[0], Shell)
        self.assertEqual(self.doer_manager.doers[0].command,
                              'echo "%f has changed."')

        self.assertIsInstance(self.doer_manager.doers[1], Shell)
        self.assertEqual(self.doer_manager.doers[1].command, 'test')

        self.assertIsInstance(self.doer_manager.doers[2], Shell)
        self.assertEqual(self.doer_manager.doers[2].command, 'echo "Bye"')

        with self.assertRaises(AttributeError):
            DoerManager(['non existant::something'], Shell)

    def test_run_doers(self):
        """Check that the doers are being run successfully.
        """
        self.assertEqual(
            self.doer_manager.run_doers('/some/random/file'),
            [
                '/some/random/file has changed.\n',
                '\nCommand failed to run, exited with error code 1',
                'Bye\n'
            ])

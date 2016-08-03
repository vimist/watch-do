import io
import os
import subprocess
import unittest
from unittest.mock import patch

from watch_do.watch_do import WatchDo, NoFilesError
from watch_do.methods.hash import Hash


class TestWatchDo(unittest.TestCase):
    @patch('os.path.isfile')
    @patch('glob.glob')
    def setUp(self, glob_glob, os_path_isfile):
        glob_glob.return_value = ['file1.py', 'file2.py', 'directory.py']
        os_path_isfile.side_effect = [True, True, False]

        self.watch_do = WatchDo(
            ['*.py'], Hash, 2, True, True, True,
            ['echo "Command 1"', 'echo "Command 2"']
        )

    def test_init(self):
        self.assertEqual(self.watch_do._globs, ['*.py'], 'globs not stored')
        self.assertEqual(self.watch_do._method, Hash, 'method not stored')
        self.assertEqual(self.watch_do._interval, 2, 'interval not stored')
        self.assertTrue(self.watch_do._clear, 'clear value not stored')

        self.assertIn(
            'echo "Command 1"', self.watch_do._commands, 'command1 not stored')
        self.assertIn(
            'echo "Command 2"', self.watch_do._commands, 'command2 not stored')

        self.assertIn('file1.py', self.watch_do._files, 'file1.py not stored')
        self.assertIn('file2.py', self.watch_do._files, 'file2.py not stored')

        with patch('glob.glob') as glob_glob:
            glob_glob.return_value = []

            with self.assertRaises(NoFilesError):
                watch_do = WatchDo(['*'], Hash, 2, True, True, True, ['date'])

    def test_expand_globbing(self):
        self.assertIn(
            'file1.py', self.watch_do._files, 'file1.py not in files list')
        self.assertIn(
            'file2.py', self.watch_do._files, 'file2.py not in files list')
        self.assertNotIn(
            'directory.py', self.watch_do._files, 'directory.py in files list')

    @patch('os.system')
    def test_clear_terminal(self, os_system):
        with patch.object(os, 'name', 'posix'):
            self.watch_do._clear_terminal()

            self.assertEqual(
                os_system.call_args[0][0], 'clear',
                'incorrect command called to clear screen for posix')

        with patch.object(os, 'name', 'nt'):
            self.watch_do._clear_terminal()

            self.assertEqual(
                os_system.call_args[0][0], 'cls',
                'incorrect command called to clear screen for nt')

    @patch('builtins.open')
    def test_set_up_watchers(self, builtins_open):
        builtins_open.side_effect = [
            io.BytesIO(b'Initial file1 content'),
            io.BytesIO(b'Initial file2 content')
        ]

        watchers = self.watch_do._set_up_watchers(['file1', 'file2'])

        self.assertEqual(
            len(watchers), 2,
            'incorrect number of watchers returned')
        self.assertIsInstance(
            watchers[0], Hash,
            'incorrect watcher type returned')
        self.assertIsInstance(
            watchers[1], Hash,
            'incorrect watcher type returned')

    def test_build_header(self):
        self.assertIn(
            '2 files', self.watch_do._build_header(),
            'incorrect number of files mentioned')

    def test_build_footer(self):
        self.assertIn(
            '"file_name"', self.watch_do._build_footer('file_name', 1.234),
            'incorrect number of files mentioned in header')
        self.assertIn(
            '1.234',
            self.watch_do._build_footer('file_name', 1.234),
            'incorrect run time mentioned')

    def test_start(self):
        pass

    @patch('sys.stdout')
    @patch('subprocess.run')
    def test_run_commands(self, subprocess_run, sys_stdout):
        subprocess_run.side_effect = [
            subprocess.CompletedProcess('echo "Hello"', returncode=0),
            subprocess.CompletedProcess('echo "Error"', returncode=1),
            subprocess.CompletedProcess('echo "Third"', returncode=0)
        ]

        self.assertFalse(self.watch_do._run_commands(
            ['echo "Hello"', 'echo "Error"', 'echo "Third"'],
        ), 'didn\'t error out on second command')

        subprocess_run.side_effect = [
            subprocess.CompletedProcess('echo "Hello"', returncode=0),
            subprocess.CompletedProcess('echo "Second"', returncode=0)
        ]

        self.assertTrue(self.watch_do._run_commands(
            ['echo "Hello"', 'echo "Second"'],
        ), 'didn\'t complete successfully')

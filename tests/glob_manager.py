"""Test the `GlobManager` class.
"""

import os
import tempfile

from unittest import TestCase

from tests.helper_functions import set_up_test_files

from watch_do import GlobManager


class TestGlobManager(TestCase):
    """Test the `GlobManager` class.
    """

    def setUp(self):
        """Set up a few temporary directories with some files.
        """
        # Create a temporary directory with a few files in
        self.temp_dir = tempfile.TemporaryDirectory()
        set_up_test_files(self.temp_dir.name)

        # Change to the temporary directory
        self.cwd = os.getcwd()
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        """Clean up the temporary files used for testing.
        """
        self.temp_dir.cleanup()
        os.chdir(self.cwd)

    def test_last_files(self):
        """Test that the `last_files` property is being correctly maintained.
        """
        glob_manager = GlobManager(['*'])
        self.assertCountEqual(glob_manager.last_files, set())

        glob_manager.get_files()
        self.assertCountEqual(
            glob_manager.last_files,
            {
                'bob.py', 'dave.txt', 'fred.txt.py', 'geoff.py', 'jim.py.txt',
                'rob.txt'
            })

    def test_get_files(self):
        """Check that globbing is working as we expect it to.

        Perform some generic globbing on the test items created and ensure
        we're getting what we expect to back.
        """
        glob_manager = GlobManager(['*'])
        self.assertCountEqual(
            glob_manager.get_files(),
            {
                'bob.py', 'dave.txt', 'fred.txt.py', 'geoff.py', 'jim.py.txt',
                'rob.txt'
            })

        glob_manager = GlobManager(['*.py'])
        self.assertCountEqual(
            glob_manager.get_files(), {'bob.py', 'fred.txt.py', 'geoff.py'})

        glob_manager = GlobManager(['*.py', '*.txt'])
        self.assertCountEqual(
            glob_manager.get_files(),
            {
                'bob.py', 'dave.txt', 'fred.txt.py', 'geoff.py', 'jim.py.txt',
                'rob.txt'
            })

        glob_manager = GlobManager(['**/*.py'])
        self.assertCountEqual(
            glob_manager.get_files(),
            {
                'bob.py',
                'fred.txt.py',
                'geoff.py',
                'animals/dog.py',
                'animals/mouse.txt.py',
                'animals/sheep.py',
                'animals/vehicles/bus.py',
                'animals/vehicles/aeroplane.txt.py',
                'animals/vehicles/tractor.py'
            })

        glob_manager = GlobManager(['bob.py'])
        self.assertCountEqual(glob_manager.get_files(), {'bob.py'})

        glob_manager = GlobManager(['bob.py', 'bob.py'])
        self.assertCountEqual(glob_manager.get_files(), {'bob.py'})

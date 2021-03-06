"""Test the `GlobManager` class.
"""

import os

from tests.helper_functions import TestCaseWithFakeFiles

from watch_do import GlobManager


class TestGlobManager(TestCaseWithFakeFiles):
    """Test the `GlobManager` class.
    """
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

        glob_manager = GlobManager(
            [os.path.join(self.temp_dir.name, file_name) for file_name in [
                'bob.py', 'geoff.py']])
        self.assertCountEqual(glob_manager.get_files(), {'bob.py', 'geoff.py'})

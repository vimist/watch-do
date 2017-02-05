"""Test the `GlobManager` class.
"""

import os
import tempfile

from unittest import TestCase

from watch_do import GlobManager

def create_file(file_name):
    """Create a file.

    Parameters:
        file_name (str): The file to create.
    """
    open(file_name, 'a').close()

class TestGlobManager(TestCase):
    """Test the `GlobManager` class.
    """

    def setUp(self):
        """Set up a few temporary directories with some files.
        """
        # Create a temporary directory with a few files in
        self.temp_dir = tempfile.TemporaryDirectory()

        create_file(os.path.join(self.temp_dir.name, 'dave.txt'))
        create_file(os.path.join(self.temp_dir.name, 'bob.py'))
        create_file(os.path.join(self.temp_dir.name, 'jim.py.txt'))
        create_file(os.path.join(self.temp_dir.name, 'fred.txt.py'))
        create_file(os.path.join(self.temp_dir.name, 'rob.txt'))
        create_file(os.path.join(self.temp_dir.name, 'geoff.py'))

        # Create a sub-directory with some files in
        self.sub_dir = os.path.join(self.temp_dir.name, 'my_directory')
        os.makedirs(self.sub_dir)

        create_file(os.path.join(self.sub_dir, 'rat.py.txt'))
        create_file(os.path.join(self.sub_dir, 'cow.txt'))
        create_file(os.path.join(self.sub_dir, 'dog.py'))
        create_file(os.path.join(self.sub_dir, 'sheep.py'))
        create_file(os.path.join(self.sub_dir, 'cat.txt'))
        create_file(os.path.join(self.sub_dir, 'mouse.txt.py'))

        # Change to the temporary directory
        self.cwd = os.getcwd()
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        """Clean up the temporary files used for testing.
        """
        self.temp_dir.cleanup()
        os.chdir(self.cwd)

    def test_get_files(self):
        """Check that globbing is working as we expect it to.

        Perform some generic globbing on the test items created and ensure
        we're getting what we expect to back.
        """
        glob_manager = GlobManager(['*'])
        self.assertEqual(
            glob_manager.get_files(),
            {
                'bob.py',
                'dave.txt',
                'fred.txt.py',
                'geoff.py',
                'jim.py.txt',
                'rob.txt'
            })

        glob_manager = GlobManager(['*.py'])
        self.assertEqual(
            glob_manager.get_files(),
            {
                'bob.py',
                'fred.txt.py',
                'geoff.py'
            })

        glob_manager = GlobManager(['*.py', '*.txt'])
        self.assertEqual(
            glob_manager.get_files(),
            {
                'bob.py',
                'dave.txt',
                'fred.txt.py',
                'geoff.py',
                'jim.py.txt',
                'rob.txt'
            })

        glob_manager = GlobManager(['**/*.py'])
        self.assertEqual(
            glob_manager.get_files(),
            {
                'my_directory/dog.py',
                'my_directory/mouse.txt.py',
                'my_directory/sheep.py'
            })

        glob_manager = GlobManager(['bob.py'])
        self.assertEqual(glob_manager.get_files(), {'bob.py'})

        glob_manager = GlobManager(['bob.py', 'bob.py'])
        self.assertEqual(glob_manager.get_files(), {'bob.py'})

"""A collection of functions that are helpful across the tests.
"""

import os
from os.path import join


def create_file(file_name, content=''):
    """Create a file.

    File contents are truncated first, so if the file exists, it will be
    overwritten with the new `content`.

    Parameters:
        file_name (str): The file to create.
        content (str): The string to write to the file.
    """
    with open(file_name, 'w') as file_handle:
        file_handle.write(content)


def remove_file(file_name):
    """Remove a file.

    Parameters:
        file_name (str): The file to remove.
    """
    os.unlink(file_name)


def set_up_test_files(directory, ):
    """Create a few test files in a temporary directory.

    A number of files are created in a test directory for the tests to use as
    fake data in order to prove globbing, change detaction and other
    functionality works as expected.

    Parameters:
        directory (str): The directory to create the test files inside.
    """
    # Create some files at the root of the given `directory`
    create_file(join(directory, 'dave.txt'))
    create_file(join(directory, 'bob.py'))
    create_file(join(directory, 'jim.py.txt'))
    create_file(join(directory, 'fred.txt.py'))
    create_file(join(directory, 'rob.txt'))
    create_file(join(directory, 'geoff.py'))

    # Create a sub-directory with some files in
    sub_dir = join(directory, 'animals')
    os.makedirs(sub_dir)

    create_file(join(sub_dir, 'rat.py.txt'))
    create_file(join(sub_dir, 'cow.txt'))
    create_file(join(sub_dir, 'dog.py'))
    create_file(join(sub_dir, 'sheep.py'))
    create_file(join(sub_dir, 'cat.txt'))
    create_file(join(sub_dir, 'mouse.txt.py'))

    # Create a sub-sub-directory with some files in
    sub_sub_dir = join(sub_dir, 'vehicles')
    os.makedirs(sub_sub_dir)

    create_file(join(sub_sub_dir, 'aeroplane.txt.py'))
    create_file(join(sub_sub_dir, 'tractor.py'))
    create_file(join(sub_sub_dir, 'van.txt'))
    create_file(join(sub_sub_dir, 'car.py.txt'))
    create_file(join(sub_sub_dir, 'bus.py'))
    create_file(join(sub_sub_dir, 'boat.txt'))

"""Test the functionality of the command line interface.
"""

import os

from unittest import TestCase
from unittest.mock import patch
from unittest.mock import PropertyMock

from watch_do.cli import get_subclasses_of
from watch_do.cli import clear_screen


class Top:
    """A temporary top level class for testing.
    """
    pass


class A(Top):
    """A temporary sub class for testing.
    """
    pass


class B(Top):
    """A temporary sub class for testing.
    """
    pass


class C:
    """A temporary sub class for testing.
    """
    pass


class fake_package:
    """A temporary class that mimics a package for testing.
    """
    Top = Top
    A = A
    B = B
    C = C


class TestCLI(TestCase):
    """Test the functionality of the command line interface.
    """

    def test_get_subclasses_of(self):
        """Check that the correct classes are returned.
        """
        self.assertCountEqual(get_subclasses_of(Top, fake_package), {A, B})

    def test_clear_screen(self):
        """Check that the correct clear screen command is sent for each OS.
        """
        with patch('os.system') as os_system:
            clear_screen()
            os_system.assert_called_with('clear')
            with patch('os.name', 'nt') as os_name:
                clear_screen()
                os_system.assert_called_with('cls')

    def test_watch_do(self):
        """Check that the main cli method works as expected.

        This is a tricky one to test as it's making use of other components
        that already have tests written for them.
        """
        pass

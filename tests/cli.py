"""Test the functionality of the command line interface.
"""

from unittest import TestCase
from unittest.mock import patch

from watch_do.cli import get_subclasses_of
from watch_do.cli import clear_screen


# pylint: disable=too-few-public-methods
class TestBaseClass:
    """A temporary top level class for testing.
    """
    pass


# pylint: disable=too-few-public-methods
class TestClassA(TestBaseClass):
    """A temporary sub class for testing.
    """
    pass


# pylint: disable=too-few-public-methods
class TestClassB(TestBaseClass):
    """A temporary sub class for testing.
    """
    pass


# pylint: disable=too-few-public-methods
class TestClassC:
    """A temporary sub class for testing.
    """
    pass


# pylint: disable=too-few-public-methods
class FakePackage:
    """A temporary class that mimics a package for testing.
    """
    test_base_class = TestBaseClass
    test_class_a = TestClassA
    test_class_b = TestClassB
    test_class_c = TestClassC


class TestCLI(TestCase):
    """Test the functionality of the command line interface.
    """

    def test_get_subclasses_of(self):
        """Check that the correct classes are returned.
        """
        self.assertCountEqual(
            get_subclasses_of(TestBaseClass, FakePackage),
            {TestClassA, TestClassB})

    # pylint: disable=no-self-use
    def test_clear_screen(self):
        """Check that the correct clear screen command is sent for each OS.
        """
        with patch('os.system') as os_system:
            clear_screen()
            os_system.assert_called_with('clear')
            with patch('os.name', 'nt'):
                clear_screen()
                os_system.assert_called_with('cls')

    def test_watch_do(self):
        """Check that the main cli method works as expected.

        This is a tricky one to test as it's making use of other components
        that already have tests written for them; it also doesn't have a return
        value.
        """
        pass

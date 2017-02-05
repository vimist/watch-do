"""Test the base `Watcher` class
"""

from unittest import TestCase
from unittest.mock import patch
import tempfile

from watch_do.watchers import Watcher


class TestWatcher(TestCase):
    """Test the base `Watcher` class
    """

    def setUp(self):
        """Create an instance of the watcher referencing a temporary file.
        """
        self.temporary_file = tempfile.NamedTemporaryFile('r')
        self.watcher = Watcher(self.temporary_file.name)

    def test___init__(self):
        """Check the temporary file's name has been stored correctly.
        """
        self.assertEqual(self.watcher.file_name, self.temporary_file.name)

    def test_has_changed(self):
        """Check the method recognises changes in values.
        """
        # Patch the _get_value to return 'Hello'
        with patch('watch_do.watchers.Watcher._get_value') as get_value:
            get_value.return_value = 'Hello'

            self.assertTrue(self.watcher.has_changed())
            # Nothing changed, so the result should be False now
            self.assertFalse(self.watcher.has_changed())

    def test__get_value(self):
        """Check this method isn't implemented in the base class.
        """
        self.assertRaises(NotImplementedError, self.watcher._get_value)

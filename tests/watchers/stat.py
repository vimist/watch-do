"""Test the `ModificationTime` watcher.
"""

import os

from unittest import TestCase
import tempfile

from watch_do.watchers import ModificationTime


class TestModificationTime(TestCase):
    """Test the `ModificationTime` watcher.
    """

    def setUp(self):
        """Create an instance of the watcher referencing a temporary file.
        """
        # No buffering, all data is written straight to the file
        self.temporary_file = tempfile.NamedTemporaryFile(buffering=0)

        # Set the modified and accessed time to 01-01-1970 00:00:00
        os.utime(self.temporary_file.name, (0, 0))

        self.modification_time = ModificationTime(self.temporary_file.name)

    def test__get_value(self):
        """Ensure that the modification time is successfully returned.
        """
        self.assertEqual(self.modification_time._get_value(), '0.0')

        os.utime(self.temporary_file.name, (0, 1234567890))

        self.assertEqual(self.modification_time._get_value(), '1234567890.0')

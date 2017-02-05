"""Test the `MD5` watcher class.
"""

from unittest import TestCase
import tempfile

from watch_do.watchers import MD5


class TestMD5(TestCase):
    """Test the `MD5` watcher class.
    """

    def setUp(self):
        """Create an instance of the watcher referencing a temporary file.
        """
        # No buffering, all data is written straight to the file
        self.temporary_file = tempfile.NamedTemporaryFile(buffering=0)
        # Set the starting value and seek to the beginning ready for reading

        self.md5 = MD5(self.temporary_file.name)

    def tearDown(self):
        """Clear up the temporary file
        """
        self.temporary_file.close()

    def test__get_value(self):
        """Check that the hashed value is correct.
        """
        self.temporary_file.write(b'Hello')
        self.temporary_file.seek(0)

        self.assertEqual(
            self.md5._get_value(), '8b1a9953c4611296a827abf8c47804d7')

        self.temporary_file.write(b'World')
        self.temporary_file.seek(0)

        self.assertEqual(
            self.md5._get_value(), 'f5a7924e621e84c9280a9a27e1bcb7f6')

        md5 = MD5('/some/made/up/file/path')
        self.assertRaises(FileNotFoundError, md5._get_value)

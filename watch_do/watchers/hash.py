"""Hash based watchers.
"""

import hashlib

from . import Watcher


class MD5(Watcher):
    """MD5 hash based change detection.

    This class uses MD5 hashes based on the files contents to enable change
    detection.
    """

    def _get_value(self):
        """Get the current MD5 hash value of the file.

        Raises:
            FileNotFoundError: If the file could not be found.

        Returns:
            str: A string representation of the MD5 hash of the file.
        """
        md5_hash = hashlib.md5()

        with open(self.file_name, 'rb') as file_handle:
            chunk = file_handle.read(4096)
            while chunk:
                md5_hash.update(chunk)
                chunk = file_handle.read(4096)

        return md5_hash.hexdigest()

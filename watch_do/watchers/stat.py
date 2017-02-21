"""Stat based watchers.
"""

import os

from . import Watcher


class ModificationTime(Watcher):
    """A modification time based watcher.

    This class uses the files modification time to enable change detection.
    """

    def _get_value(self):
        """Get the modification time of the file.

        Raises:
            FileNotFoundError: If the file could not be found.

        Returns:
            str: The modification time of the file as a unix timestamp.
        """
        mtime = os.stat(self.file_name).st_mtime
        return str(mtime)

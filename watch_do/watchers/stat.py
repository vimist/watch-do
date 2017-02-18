"""Stat based watchers.
"""

import os

from . import Watcher


class ModificationTime(Watcher):
    """A modification time based watcher.
    """

    def _get_value(self):
        """Get the modification time of the file.
        """
        mtime = os.stat(self.file_name).st_mtime
        return str(mtime)

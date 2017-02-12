"""Manage a list of glob patterns.
"""

import os
import glob


class GlobManager:
    """Manage a list of glob patterns.
    """

    def __init__(self, globs):
        self._globs = globs
        self._last_files = set()

    @property
    def globs(self):
        """Get the globs passed into this class.

        Returns:
            set: A set of globs that were passed into this class.
        """
        return self._globs

    @property
    def last_files(self):
        """Get the last files that were returned by the `get_files` method.

        Returns:
            set: A set of files last returned by the `get_files` method.
        """
        return self._last_files

    def get_files(self):
        """Expand the globs and get a list of matching files.

        Returns:
            list: A list of strings containing the matching files.
        """
        files = set()
        for glob_pattern in self.globs:
            items = glob.glob(glob_pattern, recursive=True)

            for item in items:
                if os.path.isfile(item):
                    files.add(item)

        self._last_files = files
        return files

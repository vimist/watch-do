"""Manage a list of glob patterns.
"""

import os
import glob


class GlobManager:
    """Manage a list of glob patterns.
    """

    def __init__(self, globs):
        self._globs = globs

    @property
    def globs(self):
        """Get the globs passed into this class.

        Returns:
            set: A set of globs that were passed into this class.
        """
        return self._globs

    def get_files(self):
        """Expand the globs and get a list of matching files.

        Returns:
            list: A list of strings containing the matching files.
        """
        files = []
        for glob_pattern in self.globs:
            files = files + glob.glob(glob_pattern, recursive=True)

            for file_name in files:
                if not os.path.isfile(file_name):
                    files.remove(file_name)

        files.sort()
        return set(files)

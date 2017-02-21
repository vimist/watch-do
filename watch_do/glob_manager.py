"""The :class:`.GlobManager` is responsible for expanding globs and ensuring
that **only files** are returned.

Multiple globs can be passed in to the class, these are then expanded and
matching files (no directories) are returned.

As an example, the following code would set up a :class:`.GlobManager` class
that would find all files ending in ``.py``.

>>> manager = GlobManager(['**/*.py'])

To actually get the files matching the specified globs the :meth:`get_files`
method can be called:

>>> manager.get_files()
"""

import os
import glob


class GlobManager:
    """This class expands the globs that are provided to it.

    Multiple globs can be specified in order to watch a multitude of files.
    """

    def __init__(self, globs):
        """Initialise the :class:`.GlobManager`.

        Parameters:
            globs (list): A list of globs (as strings) that this class will
                expand.
        """
        self._globs = globs
        self._last_files = set()

    @property
    def globs(self):
        """set: A ``set`` of globs that were passed into this class.
        """
        return self._globs

    @property
    def last_files(self):
        """set: The ``set`` of files last returned by the :meth:`get_files`
        method.
        """
        return self._last_files

    def get_files(self):
        """Expand the globs and return a ``set`` of matching files.

        Returns:
            set: A ``set`` of strings containing the files that matched the
            globs passed into this class.
        """
        files = set()
        for glob_pattern in self.globs:
            items = glob.glob(glob_pattern, recursive=True)

            for item in items:
                if os.path.isfile(item):
                    files.add(item)

        self._last_files = files
        return files

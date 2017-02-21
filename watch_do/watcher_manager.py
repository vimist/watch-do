"""The :class:`.WatcherManager` class is responsible for orchestrating the
watchers.

The watchers are created based on the files returned by the
:class:`.GlobManager` instance that get provided to this class. For each file
that the :class:`.GlobManager` returns a new :class:`.Watcher` is created.
Multiple options can be provided to this class that allows for some
configuration, please see the :meth:`__init__` method documentation for
details.

As an example, the following code would set up watchers for all files returned
by ``glob_manager`` using the :class:`.ModificationTime` method. Newly created
files are detected and added to the watch list and files that get deleted are
considered to be a change (this is specified as the last two parameters of the
constructor).

>>> manager = WatcherManager(
...     ModificationTime, glob_manager, True, True)

All of the changed files can be retrieved by calling :meth:`get_changed_files`.

>>> manager.get_changed_files()
"""


class WatcherManager:
    """This class creates and manages watchers.

    A :class:`.Watcher` and an instance of :class:`.GlobManager` are passed in,
    which provides the necessary information for the class to create the
    required watchers that can be used to detect changes.
    """

    def __init__(self, watcher, glob_manager, reglob, changed_on_remove):
        """Initialise the :class:`.WatcherManager`.

        Parameters:
            watcher (:class:`.Watcher`): A reference to a subclass of
                :class:`.Watcher` (i.e. :class:`.ModificationTime`) that will
                be used watch the files provided by the :class:`.GlobManager`.
            glob_manager (:class:`.GlobManager`): The glob manager responsible
                for providing a list of files.
            reglob (bool): A boolean value indicating whether to re-evaluate
               globs when :meth:`get_changed_files` is called.
            changed_on_remove (bool): A boolean value indicating whether to
              consider the removal of a file a change.
        """
        self._watcher = watcher
        self._glob_manager = glob_manager
        self._reglob = reglob
        self._changed_on_remove = changed_on_remove

        self._first_call_to_changed_files = True
        self._files = set()
        self._watchers = {}

    @property
    def watcher(self):
        """:class:`.Watcher`: A reference to the :class:`.Watcher` class that
        is being used to detect changes.
        """
        return self._watcher

    @property
    def glob_manager(self):
        """:class:`.GlobManager`: The instance of the :class:`.GlobManager`
        that was passed in.
        """
        return self._glob_manager

    @property
    def reglob(self):
        """bool: A boolean value indicating whether we are re-evaluating file
        globs each time :meth:`get_changed_files` is called.
        """
        return self._reglob

    @property
    def changed_on_remove(self):
        """bool: A boolean value indicating if removed files count as a change.
        """
        return self._changed_on_remove

    @property
    def files(self):
        """set: The ``set`` of file names (relative to the current directory)
        that are being watched.
        """
        return self._files

    def get_changed_files(self):
        """Get a ``set`` containing the changed files since the last call.

        This method determines which files have changed since the last time
        this method was called. Added files, changed files (determined by the
        type of watcher) and removed files (if `changed_on_remove` is True) are
        all counted as changed files.

        The watchers are stored and managed internally to this class.

        Returns:
            set: A ``set`` of files that have changed since the last time this
            method was called.
        """
        # Keep track of added and removed files
        added_files = set()
        removed_files = set()

        # Update the list of files we should be watching. Only do this if
        # this is the first time, or if reglob is set to True
        if self.reglob or self._first_call_to_changed_files:
            new_files = self.glob_manager.get_files()

            added_files = new_files - self._files
            removed_files = self._files - new_files

            self._files = new_files

        changed_files = set()

        # Create watchers for newly found files
        for file_name in added_files:
            self._watchers[file_name] = self.watcher(file_name)

            if not self._first_call_to_changed_files:
                changed_files.add(file_name)

        # Remove watchers for non existent files
        for file_name in removed_files:
            del self._watchers[file_name]

            if self.changed_on_remove:
                changed_files.add(file_name)

        # Check for changed files
        for watcher in self._watchers:
            try:
                if self._watchers[watcher].has_changed():
                    changed_files.add(self._watchers[watcher].file_name)
            except FileNotFoundError as ex:
                # Handle FileNotFoundError exceptions only if reglobbing is
                # False, otherwise re-raise it
                if self.reglob:
                    raise ex

        self._first_call_to_changed_files = False

        return changed_files

"""The `WatcherManager` is responsible for creating and deleting watchers.
"""


class WatcherManager:
    """The `WatcherManager` is responsible for creating and deleting watchers.
    """

    def __init__(self, watcher, glob_manager, reglob, changed_on_remove):
        """Initialise the `WatcherManager` properties.

        Properties:
            watcher (Watcher): A reference to a subclass of `Watcher` that
                               will be used watch the files provided by the
                               `GlobManager`.
            glob_manager (GlobManager): The glob manager responsible for
                                        providing a list of files.
            reglob (bool): A boolean value indicating whether to re-evaluate
                           globs when `changed_files` is called.
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
        """Get a reference to the watcher class that is being used.

        Returns:
            Watcher: A reference to the watcher class that is being used.
        """
        return self._watcher

    @property
    def glob_manager(self):
        """Get the `GlobManager` instance that's providing file names to watch.

        Returns:
            GlobManager: The instance of the `GlobManager` that was passed in.
        """
        return self._glob_manager

    @property
    def reglob(self):
        """Get the value determining whether we are re-evaluating file globs.

        Returns:
            bool: A boolean value indicating whether we are re-evaluating file
                  globs.
        """
        return self._reglob

    @property
    def changed_on_remove(self):
        """Get the value determining whether removed files count as a change.

        Returns:
            bool: A boolean value indicating if removed files count as a
                  change.
        """
        return self._changed_on_remove

    @property
    def files(self):
        """Get the set of files that are being watched.

        Returns:
            set: A set of file names (relative to the current cirectory)
                  that are being watched.
        """
        return self._files

    def get_changed_files(self):
        """Get a `set` of changed files.

        This method determines which files have changed since the last time
        this method was called. Added files, changed files (determined by the
        type of watcher) and removed files (if `changed_on_remove` is True) are
        all counted as changed files.

        The watchers are stored and managed internally to this class.

        Returns:
            set: A `set` of files that have changed since the last time this
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

        # Remove watchers for non existant files
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

"""The base `Watcher`.
"""

class Watcher:
    """The base `Watcher` that all other watchers should inherit from.

    This class enables child classes to concentrate on the change detection
    and to not have to concern themselves about how this is presented to the
    user.
    """

    def __init__(self, file_name):
        self._file_name = file_name
        self._last_value = None

        self._first_call_to_has_changed = True

    @property
    def file_name(self):
        """Get the file name that this watcher is watching.
        """
        return self._file_name

    def has_changed(self):
        """Determine if the file has changed.

        Determine if the file has changed singe the last time this
        method was called.

        Returns:
            bool: A boolean, indicating if the watched file has changed.
        """
        value = self._get_value()

        changed = True if value != self._last_value else False

        self._last_value = value

        # Always return False on the first call to `has_changed`
        if self._first_call_to_has_changed:
            self._first_call_to_has_changed = False
            changed = False

        return changed

    def _get_value(self):
        """Get the current value of the watched file.

        **Should be overwritten and implemented in child classes.**

        Determines the current change value of the file being watched. This
        could be the file's hash, the modified time, or some other value that
        can be used to determine if we should update the `changed` status.

        Returns:
            str: A value representing the current state of the object that this
            base class can use to determine if the file has changed.
        """
        raise NotImplementedError(
            'The `_get_value` method should be implemented by the child class')

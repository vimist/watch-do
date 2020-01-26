"""The :class:`.Watcher` base class is responsible for providing the high level
interface to a watcher, the actual functionality is left to the derived class.

The watchers are typically created and managed by an instance of a
:class:`.WatcherManager` class.

.. warning::
    This class cannot be instantiated directly, it is an abstract base class.
    Only derived classes that inherit from this class and implement
    :meth:`_get_value` can be instantiated.
"""

from abc import ABCMeta
from abc import abstractmethod


class Watcher(metaclass=ABCMeta):
    """This is the base :class:`.Watcher` that all other watchers should
    inherit from.

    A file name is passed in that will be monitored for changes.

    .. note::
        The file state is only checked when the :meth:`has_changed` method is
        called.
    """

    def __init__(self, file_name):
        """Initialise the :class:`.Watcher`.

        Parameters:
            file_name (str): The file path that the watcher should detect
                changes for.
        """
        self._file_name = file_name
        self._last_value = None

        self._first_call_to_has_changed = True

    @property
    def file_name(self):
        """Get the name and path of the file that this watcher is monitoring.
        """
        return self._file_name

    def has_changed(self):
        """Determine if the file has changed since the last call to this
        method.

        .. warning::
            The first call to this method will **always** return False.

        Returns:
            bool: A boolean, indicating if the watched file has changed.
        """
        value = self._get_value()

        changed = value != self._last_value

        self._last_value = value

        # Always return False on the first call to `has_changed`
        if self._first_call_to_has_changed:
            self._first_call_to_has_changed = False
            changed = False

        return changed

    @abstractmethod
    def _get_value(self):
        """Get the current value of the watched file.

        .. attention::
            This method should be overwritten and implemented in child classes.

        This method determines the current change value of the file being
        watched. This could be the file's hash, the modified time, or some
        other value that can be used to determine if we should report the file
        as changed on the next call to :meth:`has_changed`.

        Returns:
            str: A value representing the current state of the object that this
            base class can use to determine if the file has changed.
        """

"""The exceptions defined in this module are used within the Watch Do package
for reporting different error conditions.

None of the exceptions contain any extra logic, data or functionality, they
only to provide a means to handle specific types of error.
"""


class UnknownWatcher(ImportError):
    """This can be raised when a :class:`.Watcher` cannot be found.
    """

class UnknownDoer(ImportError):
    """This can be raised when a :class:`.Doer` cannot be found.
    """

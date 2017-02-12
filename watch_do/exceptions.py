"""Custom exception classes used by Watch Do.
"""


class UnknownWatcher(ModuleNotFoundError):
    """This is raised when a `Watcher` cannot be found.
    """
    pass

class UnknownDoer(ModuleNotFoundError):
    """This is raised when a `Doer` cannot be found.
    """
    pass

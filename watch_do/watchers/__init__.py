"""Watchers are different ways of determining if a file has changed

These classes all inherit from the base `Watcher` class and implement a method
of determining if a file has changed. Some of the built in examples of this are
the `Hash` and `ModifiedTime` classes.
"""

from .watcher import Watcher
from .hash import MD5
from .stat import ModificationTime

__all__ = [
    'Watcher',
    'MD5',
    'ModificationTime'
]

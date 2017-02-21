"""Watchers implement methods of determining if a file has changed.

All watchers inherit from the base :class:`.Watcher` class. This allows the
derived class to focus on performing the change detection rather than having to
implement core functionality.
"""

from .watcher import Watcher
from .hash import MD5
from .stat import ModificationTime

__all__ = [
    'Watcher',
    'MD5',
    'ModificationTime'
]

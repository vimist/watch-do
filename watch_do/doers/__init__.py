"""Doers are implementations of common functionality you might want to perform.

These classes all inherit from the base `Doer` class and implement a method
that performs an action. A built in example of this is the `Shell` class.
"""

from .doer import Doer
from .shell import Shell

__all__ = [
    'Doer',
    'Shell'
]

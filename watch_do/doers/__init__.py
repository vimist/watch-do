"""Doers implement interfaces that enable the performing of actions.

All doers inherit from the base :class:`.Doer` class. This allows the derived
class to focus on actually executing the action rather than having to implement
core functionality.
"""

from .doer import Doer
from .shell import Shell

__all__ = [
    'Doer',
    'Shell'
]

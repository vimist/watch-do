Watchers
========

.. automodule:: watch_do.watchers

The Base Class
--------------

.. automodule:: watch_do.watchers.watcher
   :members:
   :private-members:

Built-In Watchers
-----------------

These are the built-in watchers that were available for use at the time this
documentation was built.

.. note::
   The watchers below all inherit from the above :class:`.Watcher` class. This
   means that all methods and properites detailed above are also available on
   these classes below even though they aren't mentioned.

.. autoclass:: watch_do.watchers.MD5

.. autoclass:: watch_do.watchers.ModificationTime

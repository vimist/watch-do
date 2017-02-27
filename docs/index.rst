Watch Do (|release|)
====================

.. Include the README file from the index of the repository for a basic
   overview of the Watch Do project.
.. include:: ../README.rst
   :start-line: 3

Modules
=======

.. Include the description from the modules index, but exclude the toctree,
   this is just so we don't have to make the same changes in two places.
.. include:: modules/index.rst
   :start-line: 3
   :end-before: .. toctree::

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   modules/index

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

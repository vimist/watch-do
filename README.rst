Watch Do
========

Watch Do is primarily a command line utility that allows you to monitor files
for changes using a variety of different methods (:ref:`.MD5` hash of the
file, :ref:`.ModificationTime`, etc) and then perform actions based on these
changes.

The core Watch Do libraries can be used externally from the command line
utility to provide similar functionality for use in other scripts and programs.

Installation
------------

To install Watch Do, ensure you have pip installed using your distributions
package manager and then run the following command:

.. code-block:: bash

   pip install git+https://github.com/vimist/watch-do

Basic Usage
-----------

You can start making use of Watch Do right away! A basic Watch Do command can
be seen below, this watches all ``.py`` files recursively using the default
watcher (:ref:`.ModificationTime`) and then runs ``make test`` in the
directory that Watch Do was launched in.

.. code-block:: bash

   watch-do -w '**/*.py' -d 'make test'

Run ``watch-do --help`` for more information on what all of the different
command line switches do.

.. note::

   The ``-r`` (``--reglob``) switch is often useful to maintain an up-to-date
   list of files that trigger the doers to run.

Documentation
-------------

You can run the following command to find more information on the modules the
Watch Do package provides:

.. code-block:: bash

   make serve-docs

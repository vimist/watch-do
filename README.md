Documentation build, test and linting for `master` branch:

[![Build Status](https://travis-ci.org/vimist/watch-do.svg?branch=master)](https://travis-ci.org/vimist/watch-do)
[![Test Coverage](https://lima.codeclimate.com/github/vimist/watch-do/badges/coverage.svg)](https://lima.codeclimate.com/github/vimist/watch-do/coverage)
[![Code Climate](https://lima.codeclimate.com/github/vimist/watch-do/badges/gpa.svg)](https://lima.codeclimate.com/github/vimist/watch-do)

Watch Do
========

Watch Do is primarily a command line utility that allows you to monitor files
for changes and then perform actions based on these changes.

Installation
------------

To install Watch Do, ensure you have pip installed using your distributions
package manager and then run the following command:

```sh
pip install git+https://github.com/vimist/watch-do
```

Basic Usage
-----------

You can start making use of Watch Do right away! A basic Watch Do command can
be seen below, this watches all `.py` files recursively using the default
watcher (`ModificationTime`) and then runs `make test` in the directory that
Watch Do was launched in.

```sh
watch-do -w '**/*.py' -d 'make test'
```

Run `watch-do --help` for more information on what all of the different
command line switches do.

**Note:**
The `-r` (`--reglob`) switch is often useful to maintain an up-to-date list of
files that trigger the doers to run.

Documentation
-------------

You can run the following command to find more information on the modules the
Watch Do package provides:

```sh
make serve-docs
```


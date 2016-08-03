[![Build Status](https://travis-ci.org/vimist/watch-do.svg?branch=master)](https://travis-ci.org/vimist/watch-do)
[![Code Climate](https://codeclimate.com/github/vimist/watch-do/badges/gpa.svg)](https://codeclimate.com/github/vimist/watch-do)

WatchDo
=======
A command line tool to watch files and run arbitrary commands when they
change.

Usage
-----
Run unit tests for your project whenever a change in any `.py` file is
detected (using the default hash based method):

```bash
$ ./watch_do.py -w '**/*.py' -c './tests/run_tests.py'
```

    Watching 16 files for changes

    ...................
    -------------------------------------------------------------------
    Ran 19 tests in 0.018s

    OK


    Triggered from change in "tests/watch_do/methods/test_mtime.py" at
    12:03:08
    Took 0.227 seconds to run command

Extensible
----------
You define what constitutes a changed file. Just add a new file in
`./watch_do/methods`:

```bash
touch './watch_do/methods/mtime.py'
```

Create a class with the title cased version of the file name and
implement your detection method (must be called `_detect`):

```python
import os

from watch_do.methods.base_method import BaseMethod

class Mtime(BaseMethod):
    def _detect(self):
        """
        Detects a change in a file by it's modification time
        """
        mtime = False
        try:
            mtime = os.stat(self.file_name).st_mtime
        except FileNotFoundError:
            return False

        return mtime
```

Create your tests in `./tests/watch_do/methods/test_mtime.py`:

```python
import unittest
from unittest.mock import Mock, patch

from watch_do.methods.mtime import Mtime

class TestMtime(unittest.TestCase):
    @patch('os.stat')
    def setUp(self, os_stat):
        os_stat.return_value = Mock(st_mtime=123.456)

        self.mtime = Mtime('file_name')

    def test_initial_detect(self):
        self.assertEqual(self.mtime._detect_value, 123.456,
                         'invalid _detect_value')

    def test_detect(self):
        with patch('os.stat') as os_stat:
            os_stat.return_value = Mock(st_mtime=456.789)

            self.assertNotEqual(self.mtime._detect_value,
                self.mtime._detect(),
                'content change not detected')

        self.assertFalse(self.mtime._detect(),
            'non existant file not detected')
```

Now you can use it by specifying the `-m mtime` on the command line!

#! /usr/bin/env python3

import sys
from os.path import dirname
import unittest

test_discover = unittest.TestLoader()
tests = test_discover.discover(
    dirname(__file__), 'test*.py', dirname(dirname(__file__))
)

test_runner = unittest.TextTestRunner()
result = test_runner.run(tests)

sys.exit(0 if result.wasSuccessful() else 1)

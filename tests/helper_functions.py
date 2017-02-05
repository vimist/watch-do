"""Tests for the helper functions.
"""

from unittest import TestCase


from watch_do.helper_functions import diff_set

class TestDiffSet(TestCase):
    """Test the diff_set function.
    """

    def test_diff_set(self):
        """Check the function correctly diffs sets.
        """
        self.assertEqual(
            diff_set({1, 2, 3, 4}, {2, 3, 4, 5, 6}),
            {1, 5, 6})

        self.assertEqual(
            diff_set({7, 5, 2, 1}, {1, 5, 3, 6, 4, 2}),
            {7, 6, 3, 4})

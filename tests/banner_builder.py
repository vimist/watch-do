"""Test that the banners are built correctly.
"""

import time
from unittest import TestCase

from watch_do import BannerBuilder
from watch_do.watchers.hash import MD5


class TestBannerBuilder(TestCase):
    """Test that the banners are built correctly.

    The various values should be correctly interpolated.
    """

    def test_build_header(self):
        """Check the correct header is built using the supplied parameters.
        """
        files_set = {'file_a', 'file_b', 'file_c', 'file_d', 'file_e'}
        self.assertEqual(
            BannerBuilder.build_header(files_set, MD5),
            'Watching 5 files for changes using the MD5 method...\n\n')

        files_set = {'file_a'}
        self.assertEqual(
            BannerBuilder.build_header(files_set, MD5),
            'Watching 1 file for changes using the MD5 method...\n\n')

    def test_build_footer(self):
        """Check the correct footer is built using the supplied parameters.
        """
        files_set = {'file_a', 'file_b', 'file_c', 'file_d', 'file_e'}
        trigger_time = time.time()
        hms = time.strftime('%H:%M:%S', time.gmtime(trigger_time))

        changed_files = ['file_a']
        doer_time = 5.123
        self.assertEqual(
            BannerBuilder.build_footer(trigger_time, changed_files, doer_time,
                                       files_set, MD5),
            '\n\nDoers triggered at {} from: '
            'file_a\n'
            'Ran doers in 5.12 seconds.'.format(hms))

        changed_files = ['file_b', 'file_e']
        self.assertEqual(
            BannerBuilder.build_footer(trigger_time, changed_files, doer_time,
                                       files_set, MD5),
            '\n\nDoers triggered at {} from: '
            'file_b and file_e\n'
            'Ran doers in 5.12 seconds.'.format(hms))

        changed_files = ['file_a', 'file_b', 'file_e']
        doer_time = 5.127
        self.assertEqual(
            BannerBuilder.build_footer(trigger_time, changed_files, doer_time,
                                       files_set, MD5),
            '\n\nDoers triggered at {} from: '
            'file_a, file_b and file_e\n'
            'Ran doers in 5.13 seconds.'.format(hms))

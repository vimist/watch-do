"""Test the `WatcherManager` class.
"""

from tests.helper_functions import TestCaseWithFakeFiles
from tests.helper_functions import create_file
from tests.helper_functions import remove_file

from watch_do import WatcherManager
from watch_do import GlobManager
from watch_do.watchers import Watcher
from watch_do.watchers.hash import MD5


class TestWatcherManager(TestCaseWithFakeFiles):
    """Test the `WatcherManager` class.
    """
    def setUp(self):
        super(TestWatcherManager, self).setUp()

        self.glob_manager = GlobManager(['*'])
        self.watcher_manager = WatcherManager(
            MD5, self.glob_manager, True, True)

    def test___init__(self):
        """Check that all passed in properties are being stored correctly.
        """
        self.assertTrue(issubclass(self.watcher_manager.watcher, Watcher))
        self.assertIsInstance(self.watcher_manager.glob_manager, GlobManager)
        self.assertTrue(self.watcher_manager.reglob)
        self.assertTrue(self.watcher_manager.changed_on_remove)
        self.assertEqual(self.watcher_manager.files, set())

    def test_get_changed_files(self):
        """Chack that new, removed and changed files are being reported.
        """
        # No changed files to start with
        self.assertEqual(self.watcher_manager.get_changed_files(), set(''))

        # Check we have successfully globbed some files
        self.assertEqual(self.watcher_manager.files,
                         {
                             'dave.txt',
                             'bob.py',
                             'jim.py.txt',
                             'fred.txt.py',
                             'rob.txt',
                             'geoff.py'
                         })

        # New file
        create_file('something_random.jpeg')
        self.assertEqual(self.watcher_manager.get_changed_files(),
                         {'something_random.jpeg'})

        # Removed file (as `changed_on_remove` is True)
        remove_file('something_random.jpeg')
        self.assertEqual(self.watcher_manager.get_changed_files(),
                         {'something_random.jpeg'})

        # Change file
        create_file('dave.txt', 'Hello World')
        self.assertEqual(self.watcher_manager.get_changed_files(),
                         {'dave.txt'})

        # Disable changed_on_remove
        self.watcher_manager._changed_on_remove = False
        remove_file('dave.txt')
        self.assertEqual(self.watcher_manager.get_changed_files(),
                         set())

        # New file with reglob disabled
        self.watcher_manager._reglob = False
        create_file('dave.txt')
        self.assertEqual(self.watcher_manager.get_changed_files(),
                         set())

        # Removed file with reglob disabled
        remove_file('bob.py')
        self.assertEqual(self.watcher_manager.get_changed_files(),
                         set())

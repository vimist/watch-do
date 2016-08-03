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


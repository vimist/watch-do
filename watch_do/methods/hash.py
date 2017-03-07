import hashlib

from watch_do.methods.base_method import BaseMethod


class Hash(BaseMethod):
    def _detect(self):
        """
        Detects a change in a file by MD5 hashing it
        """
        md5 = hashlib.md5()
        try:
            with open(self.file_name, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break

                    md5.update(data)
        except FileNotFoundError:
            return False

        return md5.digest()

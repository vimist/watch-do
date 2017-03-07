class BaseMethod:
    def __init__(self, file_name):
        """
        @param file_name The file to monitor for changes
        """
        self._file_name = file_name
        self._detect_value = self._detect()

    @property
    def file_name(self):
        return self._file_name

    def _detect(self):
        """
        Check if the file has changed
        This method should be overridden in the child class
        """
        raise NotImplementedError(
            '_detect not implemented for method'
        )

    def has_changed(self):
        """
        Determine whether the file has changed since the last time we
        checked
        @returns A boolean value indicating whether the file has
                 changed
        """
        new_detect = self._detect()
        changed = self._detect_value != new_detect
        self._detect_value = new_detect

        return changed

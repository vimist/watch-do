import os
import time
import glob


class NoFilesError(Exception):
    """
    Raised when there are no files available
    """
    pass


class WatchDo:
    """
    Handles globbing expansion, monitoring for changed files and
    running commands
    """
    def __init__(self, globs, method, interval, clear,
                 first, header, commands):
        self._globs = globs
        self._method = method
        self._interval = interval
        self._clear = clear
        self._first = first
        self._header = header
        self._commands = commands

        # Expand the globs and raise an error if no files are found
        self._files = self._expand_globbing(self._globs)

        if len(self._files) == 0:
            raise NoFilesError()

    def _expand_globbing(self, globs):
        """
        Expands a list of globs into a list of existing files, any
        matching directories are ignored
        @param globs A list of globs
        @returns A list of existing files
        """
        files = []

        for pattern in globs:
            items = glob.glob(pattern, recursive=True)
            for item in items:
                if os.path.isfile(item):
                    files.append(item)

        return files

    def _clear_terminal(self):
        """
        Clears the terminal
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def _set_up_watchers(self, files):
        """
        Instantiates a new watcher for each file
        @param files A list of files to instantiate watchers for
        @returns A list of watchers
        """
        watchers = []
        for f in files:
            watchers.append(
                self._method(f)
            )

        return watchers

    def _build_header(self):
        """
        Build the header ready for output
        """
        header = 'Watching {number} file{plural} for changes\n'
        header = header.format(
            number=len(self._files),
            plural=('s' if len(self._files) > 1 else ''))

        return header

    def _build_footer(self, file_name, time_to_run):
        """
        Build the footer ready for output
        """
        footer = ('\nTriggered from change in "{file_name}" at {date}'
                  '\nTook {time} seconds to run command{plural}')
        footer = footer.format(
                file_name=file_name,
                date=time.strftime('%H:%M:%S'),
                time=round(time_to_run, 3),
                plural=('s' if len(self._commands) > 1 else ''))

        return footer

    def start(self):
        """
        Start the main loop and check for file changes, if any changes
        are detected, run the commands.
        """
        watchers = self._set_up_watchers(self._files)

        if self._clear:
            self._clear_terminal()

        first = self._first
        changed = False

        while True:
            for watcher in watchers:
                if first or watcher.has_changed():

                    if self._clear:
                        self._clear_terminal()

                    if self._header:
                        print(self._build_header())

                    start_time = time.time()
                    self._run_commands(self._commands)
                    changed = True

                    if self._header:
                        print(self._build_footer(
                              ('' if first else watcher.file_name),
                              time.time()-start_time))

                    first = False
                    break

            # This stops the commands being run multiple times
            # if multiple files changed very quickly
            if changed:
                for watcher in watchers:
                    watcher.has_changed()

                changed = False

            time.sleep(self._interval)

    def _run_commands(self, commands):
        """
        Run a list of commands, only continuing if all previous
        commands have successfully run
        @param commands The commands to run
        @returns A boolean value indicating if all commands were
                 successfully executed
        """
        for command in commands:
            result = os.system(command)
            return_code = result >> 8  # Highest 8 bits are exit code
            print()

            if return_code != 0:
                return False

        return True

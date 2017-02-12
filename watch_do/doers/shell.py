"""Shell based doers
"""

import subprocess

from . import Doer


class Shell(Doer):
    """A doer that will run a command in the shell and return it's output.
    """

    def run(self, file_name):
        """Run a command in the shell.

        Parameters:
            file_name (str): The file_name that this doer should run against.

        Raises:
            CalledProcessError: When the return code of the subprocess is not
                                zero.

        Returns:
            str: A string containing the output of the command, both stdout and
                 stderr.
        """
        command = Doer._interpolate_file_name(self.command, file_name)
        try:
            output = subprocess.check_output(
                command, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as ex:
            output = (
                ex.output +
                b'\nCommand failed to run, exited with error code ' +
                bytes(str(ex.returncode), 'utf-8')
            )

        return output.decode('utf-8')

"""The :class:`.Shell` class provides a method to run shell commands and
capture their output.

As an example, the following code would provide a method of getting the output
from listing a specific files attributes on the command line.

>>> doer = Shell('ls -lh "%f"')

To actually run and retrieve the output of this command, the :meth:`run` method
should be called.

>>> doer.run('myfile.txt')
"""

import subprocess

from . import Doer


class Shell(Doer):
    """Interface with a shell to allow running standard shell commands.

    This doer enables commands to be run in a shell and have the output
    captured.
    """

    def run(self, file_name):
        """Run the command in the shell.

        The :meth:`_interpolate_file_name` is called on the ``command`` with
        ``file_name`` as a parameter to ensure this ``file_name`` is
        interpolated if it's required.

        Parameters:
            file_name (str): The ``file_name`` that this doer should run
                against.

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

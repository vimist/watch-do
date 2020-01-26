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

        Yields:
            str: A string containing the output (possibly the partial output)
                of the command, both stdout and stderr.
        """
        command = Doer._interpolate_file_name(self.command, file_name)

        with subprocess.Popen(command, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, encoding='UTF-8',
                              bufsize=1, shell=True) as process:
            for line in process.stdout:
                yield line

            process.wait()

            # If the command returned a non 0 exit code, yield an error message
            if process.returncode > 0:
                yield ('Command failed to run, exited with error code {}'
                       .format(process.returncode))

"""The :class:`.Doer` base class is responsible for providing the high level
interface to a doer, the actual functionality is left to the derived class.

The doers are typically created and managed by an instance of a
:class:`.DoerManager` class.

.. warning::
   This class cannot be instantiated directly, it is an abstract base class.
   Only derived classes that inherit from this class and implement
   :meth:`run` can be instantiated.
"""

from abc import ABCMeta
from abc import abstractmethod


class Doer(metaclass=ABCMeta):
    """This is the base :class:`.Doer` that all other doers should inherit
    from.

    A command is passed in that will determine the action that should be
    performed.
    """
    def __init__(self, command):
        """Initialise the :class:`.Doer`.

        Parameters:
            command (str): The command that details what action should be
                performed.
        """
        self._command = command

    @property
    def command(self):
        """Get the command this doer is performing.
        """
        return self._command

    @staticmethod
    def _interpolate_file_name(string, file_name):
        """Interpolate the ``file_name`` into a given ``string``.

        The ``string`` parameter will be searched for ``%f`` and replaced with
        ``file_name``. Any escaped ``%f``'s will be unescaped and ignored (i.e.
        ``\\%f`` becomes ``%f``).

        Parameters:
            string (str): The string to interpolate the ``file_name`` into.
            file_name (str): The file name to insert into the ``string``.

        Returns:
            str: The input string with file name interpolated.
        """
        token = '%f'

        position = 0
        while True:
            token_position = string.find(token, position)

            # Token not found, nothing to do
            if token_position == -1:
                break
            # Escaped token, ignore it and move on
            elif string[token_position-1] == '\\':
                string = string[:token_position-1] + string[token_position:]
                position = token_position + len(token)
            # Actual token, replace with the file name
            else:
                string = (
                    string[:token_position] +
                    file_name +
                    string[token_position + len(token):]
                )
                position = token_position + len(file_name)

        return string

    @abstractmethod
    def run(self, file_name):
        """Run the doer against a specific file.

        This method runs the command passed into the constructor against a
        specific file.

        Parameters:
            file_name (str): The file name to run this doer against.

        Yields:
            str: A string containing the output (possibly the partial output)
                of the command, both stdout and stderr.
        """

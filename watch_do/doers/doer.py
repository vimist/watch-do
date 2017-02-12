"""The base `Doer`.
"""

class Doer:
    """The base `Doer` that all other doers should inherit from.

    This class enables child classes to focus on performing their action rather
    than concerning themselves with how to present their action to the user.
    """
    def __init__(self, command):
        self._command = command

    @property
    def command(self):
        """Get the command this doer is using.
        """
        return self._command

    @staticmethod
    def _interpolate_file_name(string, file_name):
        """Interpolate the file name into a given string.

        The `string` parameter will be searched for %f and replaced with
        `file_name`. Any escaped %f's will be unescaped and ignored (i.e. \\%f
        becomes %f).

        Parameters:
            string (str): The string to interpolate the `file_name` into.
            file_name (str): The file name to insert into the `string`.

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

    def run(self, file_name):
        """This is the main method that all child doers should implement.

        This method should be overridden in the child class to perform the
        action.

        Parameters:
            file_name (str): The file name for which to run this doer against.

        Returns:
            str: A string, containing the status/output of the action.
        """
        raise NotImplementedError(
            'The `run` method should be implemented by the child class')

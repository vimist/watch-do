"""This class manages the doers and commands.
"""

from importlib import import_module


class DoerManager:
    """This class manages the doers and commands.

    It is converts string commands to doer instances and then provides a simple
    interface for running them and getting their output.
    """
    def __init__(self, commands, default_doer):
        """Initialise the `DoerManager`.

        Parameters:
            commands (list): A list of strings containing the commands to
                             create doers for.
            default_doer (Doer): A reference to a doer class to use as the
                                 default doer if one is not explicitly
                                 specified.
        """
        self._commands = commands
        self._default_doer = default_doer

        self._doers = self._process_commands(self.commands)

    @property
    def commands(self):
        """Get the list of commands passed in to this instance.

        Returns:
            list: The list of commands passed in to this instance.
        """
        return self._commands

    @property
    def default_doer(self):
        """Get the default doer that should be used if `doer::` isn't found.

        Returns:
            Doer: The default doer that should be used if `doer::` isn't found.
        """
        return self._default_doer

    @property
    def doers(self):
        """Get the doers that were created from of parsing the `commands`.

        Return:
            list: A list of doers that were created from of parsing the
                  `commands`.
        """
        return self._doers

    def _process_commands(self, commands):
        """Process the `commands` and create `Doer` instances from them.

        Parameters:
            commands (list): A list of strings containing the commands to
                             parse.

        Raises:
            AttributeError: This method will raise an `AttributeError` if the
                            given doer doesn't exist.

        Returns:
            list: A list of doers that were created from the `commands`.
        """
        token = '::'

        doers = []
        for command in commands:
            if token in command:
                token_position = command.find(token)

                # Parse the doer name and command out of the string
                doer_name = command[:token_position]
                doer_name = doer_name.title().replace(' ', '')
                command_part = command[token_position+len(token):]

                # Dynamically load the doer
                doers_package = import_module('.doers', 'watch_do')
                doer = getattr(doers_package, doer_name)

                # Create the doer and append it to our list
                doers.append(doer(command_part))
            else:
                # Use the default doer for our command
                doers.append(self.default_doer(command))

        return doers

    def run_doers(self, file_name):
        """Run the doers and return their output.

        Returns:
            list: A list of strings that contain the output of the doers.
        """
        results = []
        for doer in self.doers:
            results.append(doer.run(file_name))

        return results

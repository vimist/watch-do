"""The :class:`.DoerManager` class is responsible for orchestrating the doers.

Commands for the different types of doers, for example the :class:`.Shell`
doer, are provided to this class, which are then parsed and converted to their
respective doer instances. The default doer is also taken into account for
commands that don't explicitly specify a doer.

As an example, the following code would parse out the command specified as the
first argument and create a :class:`.Shell` doer from it.

>>> manager = DoerManager(['shell:echo "%f changed!"'], Shell)

In the above case, the ``shell:`` prefix wasn't necessary, as the default doer
(the second argument) was already set to :class:`.Shell`.

All of the doers can be run by calling the :meth:`.run_doers` method.

>>> manager.run_doers('my_file.txt')
"""

from importlib import import_module

from .exceptions import UnknownDoer


class DoerManager:
    """This class creates and manages doers.

    Commands are passed in, which then get parsed and converted to instances
    of doers. All doers can be run using the :meth:`.run_doers` method with
    relevant output returned.
    """

    def __init__(self, commands, default_doer):
        """Initialise the :class:`.DoerManager` and parse all commands.

        The commands that get passed into this class are parsed (removing their
        ``doer:`` prefix if required) and have the relevant doer instances
        created for them.

        Parameters:
            commands (list): A list of strings containing the commands to
                create doers for. Each command (str) in the list of commands
                should be prefixed with ``doer:``, where 'doer' is the name of
                the doer (i.e.  ``shell``). If the command is not prefixed with
                ``doer:`` the ``default_doer`` will be used.
            default_doer (:class:`.Doer`): A reference to a doer class to use
                as the default doer if one is not explicitly specified using
                the ``doer:`` prefix.
        """
        self._commands = commands
        self._default_doer = default_doer

        self._doers = self._process_commands(self.commands)

    @property
    def commands(self):
        """list: The list of stings that this :class:`.DoerManager` is
        managing.
        """
        return self._commands

    @property
    def default_doer(self):
        """:class:`.Doer`: The doer that is used if one is explicitly specified
        in the command.
        """
        return self._default_doer

    @property
    def doers(self):
        """list: The doers that were created as a result of passing the
        commands.
        """
        return self._doers

    def _process_commands(self, commands):
        """Process the `commands` and create `Doer` instances from them.

        Parameters:
            commands (list): A list of strings containing the commands to
                 parse. See the :meth:`.__init__` documentation for details on
                 the format of each command.

        Raises:
            UnknownDoer: This method will raise an :meth:`.UnknownDoer` if the
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
                try:
                    doers_package = import_module('.doers', 'watch_do')
                    doer = getattr(doers_package, doer_name)
                except AttributeError:
                    raise UnknownDoer(doer_name)

                # Create the doer and append it to our list
                doers.append(doer(command_part))
            else:
                # Use the default doer for our command
                doers.append(self.default_doer(command))

        return doers

    def run_doers(self, file_name):
        """Run each doer in turn and yield its output.

        Yields:
            str: A string that contains the combined output of stdout and
                stderr from the doers.
        """
        for doer in self.doers:
            yield from doer.run(file_name)

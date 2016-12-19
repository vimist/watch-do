from argparse import ArgumentParser

from watch_do.watch_do import WatchDo, NoFilesError
from watch_do.argument_helper import (
    string_to_method_class,
    list_methods
)
from watch_do.methods.hash import Hash

def main():
    cli_parser = ArgumentParser()
    cli_parser.add_argument(
        '-w', '--watch', dest='files', metavar='FILE', action='append',
        required=True, help='Files to watch for changes. This can be specified '
        'multiple times to watch multiple files. Globbing is also supported, '
        'directories are ignored')
    cli_parser.add_argument(
        '-m', '--method', type=string_to_method_class, action='store',
        default=Hash, metavar='{'+(', '.join(list_methods()))+'}',
        help='The method to use when checking for file changes')
    cli_parser.add_argument(
        '-i', '--interval', type=int, action='store', default=2,
        help='Interval between checking for file changes')
    # These next three arguments may look backwards, but it makes it easier to
    # work with later on
    cli_parser.add_argument(
        '--no-clear', dest='clear', action='store_false', default=True,
        help='Don\'t clear the screen between file changes')
    cli_parser.add_argument(
        '--no-header', dest='header', action='store_false', default=True,
        help='Don\'t show the header and footer')
    cli_parser.add_argument(
        '--no-first', dest='first', action='store_false', default=True,
        help='Run COMMAND(s) straight away, before any files have changed')
    cli_parser.add_argument(
        '-c', '--command', dest='commands', metavar='COMMAND', action='append',
        required=True, help='The command to execute if the file specified meets '
        'the methods change criteria. This can be specified multiple times to run '
        'multiple commands. Commands are run in the order specified. All '
        'previous commands must run successfully for the next command to be '
        'executed')

    args = cli_parser.parse_args()

    try:
        WatchDo(
            args.files, args.method, args.interval, args.clear,
            args.first,  args.header, args.commands
        ).start()
    except NoFilesError:
        cli_parser.error('no files matched any of the given globs')
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()


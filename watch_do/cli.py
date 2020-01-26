"""Watch Do.

The command line entry points into the program.
"""

import os
import sys
import time
import argparse

from . import doers
from . import watchers
from . import GlobManager
from . import WatcherManager
from . import DoerManager
from . import BannerBuilder
from .exceptions import UnknownDoer


def get_subclasses_of(parent_class, package_to_search):
    """Get classes that inherit from `parent_class` from `module_to_search`.

    Parameters:
        parent_class (class): The class all results must inherit from.
        package_to_search (package): The package to search for classes that
             inherit from `parent_class`.

    Returns:
        set: A set containing references to the found classes.
    """
    modules = set()
    for name in dir(package_to_search):
        module = getattr(package_to_search, name)
        if (isinstance(module, type) and
                issubclass(module, parent_class) and
                module is not parent_class):
            modules.add(module)
            continue

    return modules


def clear_screen():
    """Platform independent way of clearing the terminal.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def get_cli_argument_parser(watcher_class_names, doer_class_names):
    """Parse a list of arguments into an addressable data structure.

    Parameters:
        watcher_class_names (list): A list of lower cased class names of
                                    available watchers.
        doer_class_names (list): A list of lower cased class names of
                                 available doers.

    Returns:
        argparse.Namespace: A simple class with attributes containing the
                            parsed arguments.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Watch Do, a command line utility that monitors files '
        'changes and performs actions when those changes are detected.')

    parser.add_argument(
        '-w',
        '--watch',
        metavar='glob',
        action='append',
        dest='globs',
        required=True,
        help='Any number of file globs (should be quoted to stop the shell '
        'expanding them) to expand and assign watchers to.')

    parser.add_argument(
        '-d',
        '--do',
        metavar='command',
        action='append',
        dest='commands',
        required=True,
        help='Perform an action. The format of `command` is [doer::command], '
        'for example "shell::echo \'%%f changed!\'". The `doer::` portion of '
        'the command can be omitted and `--default-doer` will be used by '
        'default. If the `command` portion contains \'::\', you MUST specify '
        'the `doer::` explicitly.')

    parser.add_argument(
        '-m',
        '--watcher-method',
        choices=[watcher for watcher in watcher_class_names],
        default='modificationtime', help='The method to determine if the file '
        'has changed.')

    parser.add_argument(
        '--default-doer',
        choices=[doer for doer in doer_class_names],
        default='shell',
        help='The doer that\'s used when \'-d\' is used.')

    parser.add_argument(
        '-i',
        '--interval',
        metavar='seconds',
        type=float,
        default=2,
        help='The interval (in seconds) between checks for changed files.')

    parser.add_argument(
        '-t',
        '--wait-time',
        metavar='seconds',
        type=float,
        default=0,
        help='The time to wait (in seconds) between detecting a change and '
        'running the doers.')

    parser.add_argument(
        '-b',
        '--disable-banners',
        default=False,
        action='store_true',
        help='Disable the header and footer that is output above and below '
        'the doers\' text')

    parser.add_argument(
        '-c',
        '--disable-clear',
        default=False,
        action='store_true',
        help='Don\'t clear the screen between file changes.')

    parser.add_argument(
        '-r',
        '--reglob',
        default=False,
        action='store_true',
        help='Re-evaluate the globs to check for new or removed files.')

    parser.add_argument(
        '-e',
        '--run-on-remove',
        default=False,
        action='store_true',
        help='Run the doer(s) when a file is removed. `--reglob` must be set, '
        'otherwise removed files won\'t be detected.')

    parser.add_argument(
        '-n',
        '--multi',
        default=False,
        action='store_true',
        help='By default, Watch Do will run the doers ONCE per group of '
        'changed files. For example, if two files change at the same time (or '
        'in a time less than `--interval`), Watch Do will only run the doers '
        'once. To change this behaviour, making each changed file trigger the '
        'doers, specify this argument. If, while the doers are running, your '
        ' files change multiple times, Watch Do will only run the doers one '
        'time per changed file, it does not queue up changes.')

    return parser

# Locally disabling some Pylint features. Ideally this wouldn't have to be
# done; however, I don't feel that there is much that would logically live
# elsewhere.
# pylint: disable=R0914,R1702,R0912,R0915
def watch_do():
    """The main entry point into the Watch Do command line program.

    This methods handles command line argument parsing and configuration of the
    various modules within Watch Do.
    """
    # Build a dict of watcher and doer names with references to their
    # respective classes
    watcher_classes = {}
    for watcher_class in get_subclasses_of(watchers.Watcher, watchers):
        watcher_classes[watcher_class.__name__.lower()] = watcher_class

    doer_classes = {}
    for doer_class in get_subclasses_of(doers.Doer, doers):
        doer_classes[doer_class.__name__.lower()] = doer_class

    # Parse the command line arguments
    parser = get_cli_argument_parser(list(watcher_classes), list(doer_classes))
    args = parser.parse_args()

    try:
        # Get the selected watcher and default doer that was given
        watcher = watcher_classes[args.watcher_method]
        default_doer = doer_classes[args.default_doer]

        # Set up the basic classes that control the main Watch Do functionality
        glob_manager = GlobManager(args.globs)
        watcher_manager = WatcherManager(
            watcher, glob_manager, args.reglob, args.run_on_remove)
        doer_manager = DoerManager(args.commands, default_doer)

        # Start the main Watch Do program loop
        first_time = True
        while True:
            try:
                changed_files = watcher_manager.get_changed_files()
            except FileNotFoundError as ex:
                print('The file "{}" was not found. We will check again in {} '
                      'seconds.'.format(ex.filename, args.interval))
                time.sleep(args.interval)
                continue

            if first_time and not args.disable_banners:
                if not args.disable_clear:
                    clear_screen()

                print(BannerBuilder.build_header(
                    glob_manager.last_files, watcher), end='')

            # If some files have changed
            if changed_files:
                trigger_time = time.time()
                time.sleep(args.wait_time)

                if not args.disable_clear:
                    clear_screen()

                if not args.disable_banners:
                    print(BannerBuilder.build_header(
                        glob_manager.last_files, watcher), end='')

                # Run the doers and print their output
                start_time = time.time()
                for file_name in changed_files:
                    for output in doer_manager.run_doers(file_name):
                        print(output, end='')
                        sys.stdout.flush()

                    if not args.multi:
                        break

                end_time = time.time()
                if not args.disable_banners:
                    print(BannerBuilder.build_footer(
                        trigger_time,
                        list(changed_files),
                        end_time - start_time,
                        glob_manager.last_files,
                        watcher), end='')

            time.sleep(args.interval)
            first_time = False
    except UnknownDoer as ex:
        parser.error('unknown doer: ' + str(ex))
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    watch_do()

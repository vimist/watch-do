"""Build the banner text that is used to display metrics.
"""

import time


class BannerBuilder:
    """Build the banner text that is used to display metrics.

    The metrics display information about the current state of Watch Do.
    """

    @staticmethod
    def build_header(files, watch_method):
        """Build the header that can be displayed

        Parameters:
            files (set): A set containing the files that are
                         currently being watched.
            watch_method (Watcher): A reference to the class that is being
                                    used to watch the files.

        Returns:
            str: A string containing the header.
        """
        header = ('Watching {number_of_files} file{plural} for changes using '
                  'the {watch_method} method...\n\n')

        return header.format(
            number_of_files=len(files),
            plural='' if len(files) == 1 else 's',
            watch_method=watch_method.__name__)

    @staticmethod
    def build_footer(trigger_time, trigger_cause,
                     doer_run_time, files, watch_method):
        """Build the header that can be displayed

        Parameters:
            trigger_time (int): A timestamp of when the doers were triggered.
            trigger_cause (list): A list of items that caused the doers to run.
            doer_run_time (double): The duration of time the doers took to run.
            files (set): A set containing the files that are currently being
                         watched.
            watch_method (Watcher): A reference to the class that is being
                                    used to watch the files.

        Returns:
            str: A string containing the footer.
        """
        if len(trigger_cause) > 1:
            trigger_cause_string = ', '.join(trigger_cause[:-1])
            trigger_cause_string += ' and ' + trigger_cause[-1]
        else:
            trigger_cause_string = trigger_cause[0]

        footer = ('\n\nDoers triggered at {trigger_time} from: '
                  '{trigger_cause}\n'
                  'Ran doers in {doer_run_time} seconds.')

        return footer.format(
            trigger_time=time.strftime('%H:%M:%S',
                                       time.gmtime(trigger_time)),
            trigger_cause=trigger_cause_string,
            doer_run_time='{:.2f}'.format(doer_run_time),
            number_of_files=len(files),
            watch_method=watch_method.__name__)

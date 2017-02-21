"""The :class:`.BannerBuilder` class is responsible for creating the banners
that are displayed when using the command line interface to Watch Do.

Headers and footers are created in a format defined within this class that make
use of the metadata that is passed into the :meth:`build_header` and
:meth:`build_footer` methods.

As an example, the following code would return a header populated with the
required metadata.

>>> BannerBuilder.build_header(
...     {'file1', 'file2'}, ModificationTime)
"""

import time


class BannerBuilder:
    """This class creates the headers and footers (banners) containing metrics
    that are used predominantly by the command line interface.
    """

    @staticmethod
    def build_header(files, watch_method):
        """Build a header from the provided metadata.

        This interpolates the metadata provided by the parameters into a
        predefined string that can be used as information to display **before**
        a change has occurred.

        Parameters:
            files (set): A ``set`` containing the files that are currently
                being watched.
            watch_method (:class:`.Watcher`): A reference to the class that is
                being used to watch the files.

        Returns:
            str: A string containing the generated header.
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
        """Build the footer from the provided metadata.

        This interpolates the metadata provided by the parameters into a
        predefined string that can be used as information to display **after**
        a change has occurred.

        Parameters:
            trigger_time (int): A timestamp of when the doers were triggered.
            trigger_cause (list): A ``list`` of items that caused the doers to
                run. This list is joined with ', ' and the second to last and
                last item joined with ' and '.
            doer_run_time (double): The duration of time the doers took to run.
            files (set): A ``set`` containing the files that are currently
                being watched.
            watch_method (:class:`.Watcher`): A reference to the class that is
                being used to watch the files.

        Returns:
            str: A string containing the generated footer.
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

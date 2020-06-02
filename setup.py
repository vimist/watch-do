"""Watch Do

A set of classes (and more specifically a command line tool that implements
these classes) that performs change detection in files and performs an action
as a result.
"""

from setuptools import setup

setup(
    name='watch-do',
    version='1.1.2',
    author='Vimist',
    description='Watch a group of files for changes and then run commands',
    url='https://github.com/vimist/watch-do',
    keywords='watch files monitor run do',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Topic :: Software Development',
        'Topic :: System'
    ],
    packages=['watch_do', 'watch_do.doers', 'watch_do.watchers'],
    entry_points={
        'console_scripts': [
            'watch-do=watch_do.cli:watch_do'
        ]
    }
)

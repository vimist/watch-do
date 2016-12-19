from setuptools import setup, find_packages

setup(
    name='watch-do',
    version='0.1.0',
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
    packages=find_packages(exclude=['tests*']),
    entry_points={
        'console_scripts': [
            'watch-do=watch_do.cli_entry_point'
        ]
    }
)

#!/usr/bin/env python

"""
Motey command line tool.

Usage:
  motey start
  motey stop
  motey restart
  motey -h | --help
  motey --version

 Options:
   -h, --help       Show this message.
   --version        Print the version.
"""

from docopt import docopt

from motey import __version__ as VERSION
from motey.core import Core


def main():
    options = docopt(__doc__, version=VERSION)

    core = Core()

    if options['start']:
        core.start()
    elif options['stop']:
        core.stop()
    elif options['restart']:
        core.restart()


if __name__ == '__main__':
    main()

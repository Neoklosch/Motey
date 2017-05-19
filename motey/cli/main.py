#!/usr/bin/env python

"""
Fog Node Prototype command line tool.

Usage:
  motey start [-d | --daemon]
  motey stop
  motey -h | --help
  motey --version

 Options:
   -d, --daemon     Start as services as daemon.
   -h, --help       Show this message.
   --version        Print the version.
"""

from docopt import docopt
import motey
from motey.core import Core
# from motey import __version__ as VERSION

def main():
    options = docopt(__doc__, version='0.1')
    print(options)

    if options['start']:
        if options['--daemon']:
            print("start as daemon")
        else:
            print("start normal")
        print("starting my shit")
    elif options['stop']:
        print('stopping my shit')


if __name__ == '__main__':
    main()

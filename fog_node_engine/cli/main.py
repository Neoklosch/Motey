#!/usr/bin/env python

"""
Fog Node Prototype command line tool.

Usage:
  fognode start
  fognode stop
  fognode -h | --help
  fognode --version

 Options:
   -h, --help       Show this message.
   --version        Print the version.
"""

from docopt import docopt
from inspect import getmembers, isclass
# from fog_node_engine import __version__ as VERSION

def main():
    options = docopt(__doc__, version='0.1')
    print(options)

    if options['start']:
        print("starting my shit")
    elif options['stop']:
        print('stopping my shit')


if __name__ == '__main__':
    main()

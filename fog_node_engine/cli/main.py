#!/usr/bin/env python

"""
Fog Node Prototype command line tool.

Usage:
  fognode start [-d | --daemon]
  fognode stop
  fognode -h | --help
  fognode --version

 Options:
   -d, --daemon     Start as services as daemon.
   -h, --help       Show this message.
   --version        Print the version.
"""

from docopt import docopt
import fog_node_engine
from fog_node_engine.core import Core
# from fog_node_engine import __version__ as VERSION

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

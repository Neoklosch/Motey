#!/usr/bin/env python

"""
Capability event command line tool.

Usage:
  addcapability.py --capability=<capability> [--type=<capabilityevent>] [--action=<add|remove>]
  addcapability.py -h | --help | --version
"""


import json
import signal
import sys

import zmq
from docopt import docopt
from time import sleep

context = zmq.Context()
publisher = context.socket(zmq.PUB)


def signal_handler(signal, frame):
    print('shutdown')
    sys.exit(0)


def main():
    options = docopt(__doc__, version='0.0.1')
    publisher.connect('tcp://localhost:5090')
    # sleep is important because the connection took some time, but the publisher will immediately send out data
    sleep(2)
    json_data = [
        {'capability': options['--capability'], 'capability_type': options['--type'] if options['--type'] else 'capabilityevent', 'action': options['--action'] if options['--action'] else 'add'}
    ]
    output = 'capabilityevent#%s' % json.dumps(json_data)
    print('will send > %s' % output)
    publisher.send_string(output)



if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()

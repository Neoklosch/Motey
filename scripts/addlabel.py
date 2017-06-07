#!/usr/bin/env python

"""
Labeling event command line tool.

Usage:
  addlabel.py --label=<label> [--type=<labelingevent>] [--action=<add|remove>]
  addlabel.py -h | --help | --version
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
        {'label': options['--label'], 'label_type': options['--type'] if options['--type'] else 'labelingevent', 'action': options['--action'] if options['--action'] else 'add'}
    ]
    output = 'labelingevent#%s' % json.dumps(json_data)
    print('will send > %s' % output)
    publisher.send_string(output)



if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()

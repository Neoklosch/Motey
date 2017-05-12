import sys
import signal
from prototype.core import Core
from prototype.api.apiserver import APIServer


core = apiserver = None


def signal_handler(signal, frame):
    if core:
        core.stop()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    core = Core()
    core.start()

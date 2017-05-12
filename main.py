import sys
import signal
from prototype.core import Core
from prototype.api.apiserver import APIServer


webserver = None


def signal_handler(signal, frame):
    if webserver:
        webserver.stop()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    webserver = APIServer.Instance()
    webserver.start()

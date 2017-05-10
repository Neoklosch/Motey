import threading
from flask import Flask
from prototype.api.routes.blueprintendpoint import BlueprintEndpoint
from prototype.config import config
from prototype.utils.heartbeat import register_callback, register_heartbeat


def check_heartbeat():
    return False


class APIServer(threading.Thread):
    def __init__(self, logger):
        threading.Thread.__init__(self)
        self.logger = logger
        self.webserver = Flask(__name__)
        register_callback(check_heartbeat)
        register_heartbeat(self.webserver)
        self.configure_url()

    def run(self):
        self.logger.info('Webserver started')
        self.webserver.run(host=config['WEBSERVER']['ip'], port=config['WEBSERVER']['port'], use_reloader=False)

    def configure_url(self):
        self.webserver.add_url_rule('/hello', view_func=BlueprintEndpoint.as_view('blueprintendpoint'))

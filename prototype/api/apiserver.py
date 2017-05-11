import threading
from flask import Flask, request
from prototype.api.routes.blueprintendpoint import BlueprintEndpoint
from prototype.config import config
from prototype.utils.heartbeat import register_callback, register_heartbeat


class APIServer(threading.Thread):
    def __init__(self, logger):
        threading.Thread.__init__(self)
        self.logger = logger
        self.webserver = Flask(__name__)
        self.configure_url()

    def run(self):
        self.logger.info('Webserver started')
        self.webserver.run(host=config['WEBSERVER']['ip'], port=config['WEBSERVER']['port'], use_reloader=False)

    def configure_url(self):
        self.webserver.add_url_rule('/hello', view_func=BlueprintEndpoint.as_view('blueprintendpoint'))
        register_callback(self.check_heartbeat)
        register_heartbeat(self.webserver)

    def is_running(self):
        return request.environ.get('werkzeug.server.shutdown') is not None

    # def stop(self):
    #     if not self.is_running():
    #         return None
    #         # raise RuntimeError('Not running with the Werkzeug Server')
    #     print("stop webserver")
    #     request.environ.get('werkzeug.server.shutdown')()

    def check_heartbeat(self):
        return self.is_running()

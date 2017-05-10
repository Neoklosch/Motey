import threading
from flask import Flask
from api.routes.blueprintendpoint import BlueprintEndpoint
from config import config


class APIServer(threading.Thread):
    def __init__(self, logger):
        threading.Thread.__init__(self)
        self.logger = logger
        self.webserver = Flask(__name__)
        self.webserver.add_url_rule('/hello', view_func=BlueprintEndpoint.as_view('blueprintendpoint'))

    def run(self):
        self.logger.info('Webserver started')
        self.webserver.run(host=config['WEBSERVER']['ip'], port=config['WEBSERVER']['port'], use_reloader=False)

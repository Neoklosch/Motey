import threading
from flask import Flask
from flask_restful import Api
from api.routes.blueprintendpoint import BlueprintEndpoint
from config import config


class APIServer(threading.Thread):
    def __init__(self, logger):
        threading.Thread.__init__(self)
        self.logger = logger
        self.webserver = Flask(__name__)
        self.api = Api(self.webserver)
        self.api.add_resource(BlueprintEndpoint, '/hello')

    def run(self):
        self.logger.info('Webserver started')
        self.webserver.run(host=config['WEBSERVER']['ip'], port=config['WEBSERVER']['port'], use_reloader=False)

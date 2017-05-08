import threading
from flask import Flask
from api.routes import routes
from config import config

webserver = Flask(__name__)
webserver.register_blueprint(routes)

class APIServer(threading.Thread):
    def __init__(self, logger):
        threading.Thread.__init__(self)
        self.logger = logger

    def run(self):
        self.logger.info('Webserver started')
        webserver.run(host=config['WEBSERVER']['ip'], port=config['WEBSERVER']['port'], use_reloader=False)

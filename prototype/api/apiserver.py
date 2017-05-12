from sanic import Sanic
from prototype.config import config
from prototype.decorators.singleton import Singleton
from prototype.utils.logger import Logger
from prototype.core import Core
from prototype.api.routes.blueprintendpoint import blueprintendpoint


@Singleton
class APIServer(object):
    def __init__(self):
        self.logger = Logger.Instance()
        self.webserver = Sanic(__name__)
        self.configure_url()
        self.core = Core.Instance()
        self.webserver.listeners['after_server_start'].append(self.core.start)
        self.webserver.listeners['before_server_stop'].append(self.core.stop)

    def start(self):
        self.logger.info('Webserver started')
        self.webserver.run(host=config['WEBSERVER']['ip'], port=config['WEBSERVER']['port'])

    def stop(self):
        self.logger.info('Webserver stopped')
        self.webserver.stop()

    def configure_url(self):
        self.webserver.blueprint(blueprintendpoint)
        # self.webserver.add_url_rule('/hello', view_func=BlueprintEndpoint.as_view('blueprintendpoint'))
        # self.webserver.add_url_rule('/capabilities', view_func=Capabilities.as_view('capabilities'))
        # register_callback(self.check_heartbeat)
        # register_heartbeat(self.webserver)
        pass

    def is_running(self):
        pass
        # return request.environ.get('werkzeug.server.shutdown') is not None

    # def stop(self):
    #     if not self.is_running():
    #         return None
    #         # raise RuntimeError('Not running with the Werkzeug Server')
    #     print("stop webserver")
    #     request.environ.get('werkzeug.server.shutdown')()

    def check_heartbeat(self):
        # return self.is_running()
        pass

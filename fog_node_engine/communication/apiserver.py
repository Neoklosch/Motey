import threading
from flask import Flask, request
from fog_node_engine.communication.api_routes.blueprintendpoint import BlueprintEndpoint
from fog_node_engine.communication.api_routes.capabilities import Capabilities
from fog_node_engine.communication.api_routes.nodestatus import NodeStatus
from fog_node_engine.configuration.configreader import config
from fog_node_engine.utils.heartbeat import register_callback, register_heartbeat
from fog_node_engine.decorators.singleton import Singleton
from fog_node_engine.utils.logger import Logger


@Singleton
class APIServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.logger = Logger.Instance()
        self.webserver = Flask(__name__)
        self.configure_url()

    def run(self):
        self.logger.info('Webserver started')
        self.webserver.run(host=config['WEBSERVER']['ip'], port=config['WEBSERVER']['port'], use_reloader=False)

    def configure_url(self):
        self.webserver.add_url_rule('/blueprint', view_func=BlueprintEndpoint.as_view('blueprintendpoint'))
        self.webserver.add_url_rule('/capabilities', view_func=Capabilities.as_view('capabilities'))
        self.webserver.add_url_rule('/nodestatus', view_func=NodeStatus.as_view('nodestatus'))
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

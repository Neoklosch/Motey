import threading

from flask import Flask, request

from motey.communication.api_routes.capabilities import Capabilities
from motey.communication.api_routes.nodestatus import NodeStatus
from motey.communication.api_routes.service import Service
from motey.communication.api_routes.nodes import Nodes
from motey.utils.heartbeat import register_callback, register_heartbeat


class APIServer(object):
    """
    Starts a Flask webserver which acts as an REST API to control the Motey service.
    The webserver runs in a separate thread and will not block the main thread.
    """

    def __init__(self, logger, host='127.0.0.1', port=5023):
        """
        Constructor of the webserver.

        :param logger: the DI injected logger instance
        :param host: the hostname to listen on. Set this to ``'0.0.0.0'`` to
                     have the server available externally as well. Defaults to
                     ``'127.0.0.1'``.
        :param port: the port of the webserver. Defaults to ``5023``.
        """
        self.host = host
        self.port = port
        self.logger = logger
        self.webserver = Flask(__name__)
        self.configure_url()
        self.run_server_thread = threading.Thread(target=self.run_server, args=())
        self.run_server_thread.daemon = True

    def start(self):
        """
        Starts the execution thread.
        """
        self.run_server_thread.start()

    def run_server(self):
        """
        Starts the server and add an info to the logs, that the webserver is started.
        """
        self.logger.info('Webserver started')
        self.webserver.run(host=self.host, port=self.port, use_reloader=False)

    def configure_url(self):
        """
        Adds all the configured api endpoints.
        """
        self.webserver.add_url_rule('/v1/capabilities', view_func=Capabilities.as_view('capabilities'))
        self.webserver.add_url_rule('/v1/nodestatus', view_func=NodeStatus.as_view('nodestatus'))
        self.webserver.add_url_rule('/v1/service', view_func=Service.as_view('service'))
        self.webserver.add_url_rule('/v1/nodes', view_func=Nodes.as_view('nodes'))
        register_callback(self.check_heartbeat)
        register_heartbeat(self.webserver)

    def is_running(self):
        """
        Checks if the webserver is still running.
        :return: True if the server is running, otherwise False.
        """
        return request.environ.get('werkzeug.server.shutdown') is not None

    def stop(self):
        """
        Stops the webserver and add an info the logs, that the webserver is stopped.
        """
        self.logger.info('Webserver stopped')

    def check_heartbeat(self):
        """
        Method to get the heartbeat.
        Checks if all the requirements for a healthy webserver are fulfilled.
        :return: True if the service is in a healthy state, otherwise False.
        """
        return self.is_running()

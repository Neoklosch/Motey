from time import sleep

from daemonize import Daemonize

from motey.configuration.configreader import config


class Core(object):
    """
    This module provides the core functionality of Motey.
    It can be executed as a daemon service or can be executed in foreground.
    It will start an API webserver and a MQTTServer which can be configured via the config.ini file.
    The core will also start all the necessary components like the VALManager, the InterNodeOrchestrator and the
    HardwareEventEngine.
    After it is started via self.start() it will be executed until self.stop() is executed.
    """

    def __init__(self, logger, capability_repository, nodes_repository, valmanager, inter_node_orchestrator,
                 communication_manager, hardware_event_engine, as_daemon=True):
        """
        Constructor of the core.

        :param logger: DI injected
        :type logger: motey.utils.logger.Logger
        :param capability_repository: DI injected
        :type capability_repository: motey.repositories.capability_repository.CapabilityRepository
        :param nodes_repository: DI injected
        :type nodes_repository: motey.repositories.nodes_repository.NodesRepository
        :param valmanager: DI injected
        :type valmanager: motey.val.valmanager.VALManager
        :param inter_node_orchestrator: DI injected
        :type inter_node_orchestrator: motey.orchestrator.inter_node_orchestrator.InterNodeOrchestrator
        :param communication_manager: DI injected
        :type communication_manager: motey.communication.communication_manger.CommunicationManger
        :param hardware_event_engine: DI injected
        :type hardware_event_engine: motey.capabilityengine.capability_engine.CapabilityEngine
        :param as_daemon: Executes the core as a daemon. Default is True.
        """

        self.as_daemon = as_daemon
        self.stopped = False
        self.daemon = None

        self.logger = logger
        self.logger.info("App started")
        self.communication_manager = communication_manager
        self.capability_repository = capability_repository
        self.nodes_repository = nodes_repository
        self.valmanager = valmanager
        self.inter_node_orchestrator = inter_node_orchestrator
        self.hardware_event_engine = hardware_event_engine

    def start(self):
        """
        Start the core component. At first clean up config if necessary.
        If self.as_daemon is set to True, the component will be started as a daemon services.
        It will use the path to the pid which is configured in the config.ini.
        If self.as_daemon is set to False, the component will be executed in foreground.
        """

        self.startup_clean()
        if self.as_daemon:
            self.daemon = Daemonize(app=config['GENERAL']['app_name'], pid=config['GENERAL']['pid'], action=self.run)
            self.daemon.start()
        else:
            self.run()

    def run(self):
        """
        The method is the main app loop.
        It starts the ``Communication Manager Components`` and it will be executed until ``self.stop()`` is executed.
        """

        self.logger.info('Core started')
        self.communication_manager.start()
        self.hardware_event_engine.start()
        self.valmanager.start()

        while not self.stopped:
            sleep(.1)

    def restart(self):
        """
        Restart the core.
        """

        self.stop()
        self.start()

    def stop(self):
        """
        Clean up the started services.
        It will stop the ``Communication Manager Components``.
        Finally it stops the daemon if self.as_daemon is set to True.
        """

        self.stopped = True
        self.valmanager.close()
        self.communication_manager.stop()
        if self.daemon:
            self.daemon.exit()
        self.logger.info('Core stopped')

    def startup_clean(self):
        """
        Clean up the capability and node database to remove old entries.
        """
        self.capability_repository.clear()
        self.nodes_repository.clear()

import dependency_injector.containers as containers
import dependency_injector.providers as providers
from yapsy.PluginManager import PluginManager

from motey.communication.apiserver import APIServer
from motey.communication.communication_manager import CommunicationManager
from motey.communication.mqttserver import MQTTServer
from motey.communication.zeromq_server import ZeroMQServer
from motey.configuration.configreader import config
from motey.core import Core
from motey.capabilityengine.capability_engine import CapabilityEngine
from motey.orchestrator.inter_node_orchestrator import InterNodeOrchestrator
from motey.repositories.capability_repository import CapabilityRepository
from motey.repositories.nodes_repository import NodesRepository
from motey.repositories.service_repository import ServiceRepository
from motey.utils.logger import Logger
from motey.val.valmanager import VALManager


class DICore(containers.DeclarativeContainer):
    logger = providers.Singleton(Logger)


class DIRepositories(containers.DeclarativeContainer):
    capability_repository = providers.Singleton(CapabilityRepository)
    nodes_repository = providers.Singleton(NodesRepository)
    service_repository = providers.Singleton(ServiceRepository)


class DIServices(containers.DeclarativeContainer):
    plugin_manager = PluginManager()

    valmanager = providers.Singleton(VALManager,
                                     logger=DICore.logger,
                                     capability_repository=DIRepositories.capability_repository,
                                     plugin_manager=plugin_manager)

    zeromq_server = providers.Singleton(ZeroMQServer,
                                        logger=DICore.logger,
                                        valmanager=valmanager)

    api_server = providers.Singleton(APIServer,
                                     logger=DICore.logger,
                                     host=config['WEBSERVER']['ip'],
                                     port=config['WEBSERVER']['port'])

    mqtt_server = providers.Singleton(MQTTServer,
                                      logger=DICore.logger,
                                      nodes_repository=DIRepositories.nodes_repository,
                                      host=config['MQTT']['ip'],
                                      port=int(config['MQTT']['port']),
                                      username=config['MQTT']['username'],
                                      password=config['MQTT']['password'],
                                      keepalive=int(config['MQTT']['keepalive']))

    communication_manager = providers.Singleton(CommunicationManager,
                                                api_server=api_server,
                                                mqtt_server=mqtt_server,
                                                zeromq_server=zeromq_server)

    capability_engine = providers.Singleton(CapabilityEngine,
                                            logger=DICore.logger,
                                            capability_repository=DIRepositories.capability_repository,
                                            communication_manager=communication_manager)

    inter_node_orchestrator = providers.Singleton(InterNodeOrchestrator,
                                                  logger=DICore.logger,
                                                  valmanager=valmanager,
                                                  service_repository=DIRepositories.service_repository,
                                                  capability_repository=DIRepositories.capability_repository,
                                                  node_repository=DIRepositories.nodes_repository,
                                                  communication_manager=communication_manager)


class Application(containers.DeclarativeContainer):
    core = providers.Callable(Core,
                              logger=DICore.logger,
                              capability_repository=DIRepositories.capability_repository,
                              nodes_repository=DIRepositories.nodes_repository,
                              valmanager=DIServices.valmanager,
                              inter_node_orchestrator=DIServices.inter_node_orchestrator,
                              communication_manager=DIServices.communication_manager,
                              capability_engine=DIServices.capability_engine)

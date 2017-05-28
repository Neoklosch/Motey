import dependency_injector.containers as containers
import dependency_injector.providers as providers
from yapsy.PluginManager import PluginManager

from motey.core import Core
from motey.labelingengine.labelingengine import LabelingEngine
from motey.orchestrator.inter_node_orchestrator import InterNodeOrchestrator
from motey.repositories.labeling_repository import LabelingRepository
from motey.repositories.nodes_repository import NodesRepository
from motey.repositories.service_repository import ServiceRepository
from motey.utils.logger import Logger
from motey.val.valmanager import VALManager


class DICore(containers.DeclarativeContainer):
    logger = providers.Singleton(Logger)


class DIRepositories(containers.DeclarativeContainer):
    labeling_repository = providers.Singleton(LabelingRepository)
    nodes_repository = providers.Singleton(NodesRepository)
    service_repository = providers.Singleton(ServiceRepository)


class DIServices(containers.DeclarativeContainer):
    labeling_engine = providers.Singleton(LabelingEngine, logger=DICore.logger,
                                          labeling_repository=DIRepositories.labeling_repository)
    plugin_manager = PluginManager()
    valmanager = providers.Singleton(VALManager, logger=DICore.logger,
                                     labeling_engine=DIRepositories.labeling_repository, plugin_manager=plugin_manager)
    inter_node_orchestrator = providers.Singleton(InterNodeOrchestrator, logger=DICore.logger, valmanager=valmanager,
                                                  service_repository=DIRepositories.service_repository,
                                                  labeling_repository=DIRepositories.labeling_repository)


class Application(containers.DeclarativeContainer):
    core = providers.Callable(Core, logger=DICore.logger, labeling_repository=DIRepositories.labeling_repository,
                              nodes_repository=DIRepositories.nodes_repository, valmanager=DIServices.valmanager,
                              inter_node_orchestrator=DIServices.inter_node_orchestrator,
                              hardware_event_engine=DIServices.labeling_engine)

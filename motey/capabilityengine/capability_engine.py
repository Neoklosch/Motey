import json

from jsonschema import validate, ValidationError

from motey.models.capability import Capability
from motey.models.schemas import capability_json_schema


class CapabilityEngine(object):
    """
    This module provides a connection endpoint for third party apps like the hardware layer to add new capabilities.
    """

    def __init__(self, logger, capability_repository, communication_manager):
        """
        Constructor the the capability engine.

        :param logger: DI injected
        :type logger: motey.utils.logger.Logger
        :param capability_repository: DI injected
        :type capability_repository: motey.repositories.capability_repository.CapabilityRepository
        :param communication_manager: DI injected
        :type communication_manager: motey.communication.communication_manager.CommunicationManager
        """

        self.logger = logger
        self.capability_repository = capability_repository
        self.communication_manager = communication_manager

    def start(self):
        """
        Subscibes to the capability event stream.
        """

        self.communication_manager.add_capability_event_stream.subscribe(self.perform_add_capability)
        self.communication_manager.remove_capability_event_stream.subscribe(self.perform_remove_capability)
        self.logger.info('capability engine started')

    def stop(self):
        """
        Should be executed to clean up the capability engine
        """

        self.communication_manager.add_capability_event_stream.dispose()
        self.communication_manager.remove_capability_event_stream.dispose()
        self.logger.info('capability engine stopped')

    def parse_capability(self, data):
        """
        Parse a JSON string with capability data and transform them into an array with capability models

        :param data: the data that should be parsed
        :param data: str
        :return: an array with capability models or an empty array if something went wrong
        """
        output = []
        try:
            json_result = json.loads(data)
            validate(json_result, capability_json_schema)
            for entry in json_result:
                capability_entry = Capability.transform(entry)
                output.append(capability_entry)
        except (ValidationError, json.JSONDecodeError):
            pass
        return output

    def perform_add_capability(self, data):
        """
        Adds a capability entry to the database.

        :param data: the capability entry which should be added.
                      The entry must match the `motey.models.schemas.capability_json_schema`
        :type data: str
        """

        results = self.parse_capability(data=data)
        for entry in results:
            self.capability_repository.add(capability=entry.capability, capability_type=entry.capability_type)

    def perform_remove_capability(self, data):
        """
        Removes a capability entry from the database.

        :param data: the capability entry which should be removed.
                      The entry must match the `motey.models.schemas.capability_json_schema`
        :type data: str
        """

        results = self.parse_capability(data=data)
        for entry in results:
            self.capability_repository.remove(capability=entry.capability, capability_type=entry.capability_type)

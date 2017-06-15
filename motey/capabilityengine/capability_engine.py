import json

from jsonschema import validate, ValidationError

from motey.models.schemas import capability_action_json_schema


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
        self.communication_manager.after_capabilities_request = self.handle_capabilities_request

    def start(self):
        """
        Subscibes to the capability event stream.
        """

        self.communication_manager.capability_event_stream.subscribe(self.handle_capability_event)
        self.logger.info('capability engine started')

    def stop(self):
        """
        Should be executed to clean up the capability engine
        """

        self.communication_manager.capability_event_stream.unsubscribe()
        self.logger.info('capability engine stopped')

    def handle_capability_event(self, data):
        """
        Private function which is be executed after an event is received.
        After receiving an event a new capability will be added to the capability database.

        :param data: the received data
        """

        try:
            json_result = json.loads(data)
            if isinstance(json_result, list):
                for entry in json_result:
                    self.__perform_capability_action(entry)
            elif isinstance(json_result, dict):
                self.__perform_capability_action(json_result)
        except (TypeError, json.JSONDecodeError):
            pass

    def handle_capabilities_request(self, capabilities_replier):
        capabilities_replier.send_string(json.dumps(self.capability_repository.all()))

    def __perform_capability_action(self, entry):
        """
        Perform a specific action for the given entry.
        Possible action types are `add` and `remove`.

        :param entry: the capability entry which should be used to perform the action.
                      The entry must match the `motey.models.schemas.capability_action_json_schema`
        """

        try:
            validate(entry, capability_action_json_schema)
            if entry['action'] == 'add':
                self.capability_repository.add(capability=entry['capability'], capability_type=entry['capability_type'])
            elif entry['action'] == 'remove':
                self.capability_repository.remove(capability=entry['capability'], capability_type=entry['capability_type'])
        except ValidationError:
            pass

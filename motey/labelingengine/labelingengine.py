import json

from jsonschema import validate, ValidationError


class LabelingEngine(object):
    """
    This module provides a connection endpoint for the hardware layer.
    New labels can be added via a ZeroMQ tcp publisher which is defined in the ``ZeroMQServer``.
    """

    # JSON schema for a valid label entry
    json_schema = {
        "type": "object",
        "properties": {
            "label": {
                "type": "string"
            },
            "label_type": {
                "type": "string"
            },
            "action": {
                "enum": ["add", "remove"]
            }
        },
        "required": ["label", "label_type", "action"]
    }

    def __init__(self, logger, labeling_repository, zeromq_server):
        """
        Constructor the the labeling engine.

        :param logger: DI injected
        :type logger: motey.utils.logger.Logger
        :param labeling_repository: DI injected
        :type labeling_repository: motey.repositories.labeling_repository.LabelingRepository
        :param zeromq_server: DI injected
        :type zeromq_server: motey.communication.zeromq_server.ZeroMQServer
        """

        self.logger = logger
        self.labeling_repository = labeling_repository
        self.zeromq_server = zeromq_server
        self.zeromq_server.after_capabilities_request = self.handle_capabilities_request

    def start(self):
        """
        Subscibes to the ``ZeroMQServer`` event stream.
        """

        self.zeromq_server.capability_event_stream.subscribe(self.handle_capability_event)
        self.logger.info('labeling engine started')

    def stop(self):
        """
        Should be executed to clean up the labeling engine
        """

        self.zeromq_server.capability_event_stream.unsubscribe()
        self.logger.info('labeling engine stopped')

    def handle_capability_event(self, data):
        """
        Private function which is be executed after an event is received.
        After receiving an event a new label will be added to the LabelingDatabase.

        :param data: the received data
        """

        try:
            json_result = json.loads(data)
            if isinstance(json_result, list):
                for entry in json_result:
                    self.__perform_label_action(entry)
            elif isinstance(json_result, dict):
                self.__perform_label_action(json_result)
        except (TypeError, json.JSONDecodeError):
            pass

    def handle_capabilities_request(self, capabilities_replier):
        capabilities_replier.send_string(json.dumps(self.labeling_repository.all()))

    def __perform_label_action(self, entry):
        """
        Perform a specific action for the given entry.
        Possible action types are `add` and `remove`.

        :param entry: the label entry which should be used to perform the action. The entry must match the `json_schema`
        """

        try:
            validate(entry, self.json_schema)
            if entry['action'] == 'add':
                self.labeling_repository.add(label=entry['label'], label_type=entry['label_type'])
            elif entry['action'] == 'remove':
                self.labeling_repository.remove(label=entry['label'], label_type=entry['label_type'])
        except ValidationError:
            pass

import unittest
from unittest import mock

from rx.subjects import Subject

from motey.capabilityengine.capability_engine import CapabilityEngine
from motey.communication.communication_manager import CommunicationManager
from motey.models.capability import Capability
from motey.repositories.capability_repository import CapabilityRepository
from motey.utils.logger import Logger


class TestCapabilityEngine(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.logger = mock.Mock(Logger)
        self.capability_repository = mock.Mock(CapabilityRepository)
        self.communication_manager = mock.Mock(CommunicationManager)
        self.communication_manager.add_capability_event_stream = mock.Mock(Subject)
        self.communication_manager.remove_capability_event_stream = mock.Mock(Subject)
        self.capability_engine = CapabilityEngine(logger=self.logger,
                                                  capability_repository=self.capability_repository,
                                                  communication_manager=self.communication_manager)

    def assertCapabilityEqual(self, left, right):
        for left_entry, right_entry in zip(left, right):
            if left_entry.capability != right_entry.capability:
                raise AssertionError("capability don't match")
            if left_entry.capability_type != right_entry.capability_type:
                raise AssertionError("capability type don't match")

    def test_start(self):
        self.capability_engine.start()

        self.assertTrue(self.communication_manager.add_capability_event_stream.subscribe.called)
        self.assertTrue(self.communication_manager.remove_capability_event_stream.subscribe.called)
        self.assertTrue(self.logger.info.called)

    def test_stop(self):
        self.capability_engine.stop()

        self.assertTrue(self.communication_manager.add_capability_event_stream.dispose.called)
        self.assertTrue(self.communication_manager.remove_capability_event_stream.dispose.called)
        self.assertTrue(self.logger.info.called)

    def test_parse_capability(self):
        expected_result = [Capability(capability='test capability', capability_type='test capability type')]
        result = self.capability_engine\
            .parse_capability('[{"capability": "test capability", "capability_type": "test capability type"}]')

        self.assertCapabilityEqual(result, expected_result)

    def test_parse_capability_wrong_schema(self):
        expected_result = []
        result = self.capability_engine\
            .parse_capability('[{"wrong_parameter": "test capability", "also_wrong": "test capability type"}]')

        self.assertCapabilityEqual(result, expected_result)

    def test_parse_capability_bad_json(self):
        expected_result = []
        result = self.capability_engine\
            .parse_capability('[}wrong_json')

        self.assertCapabilityEqual(result, expected_result)

    def test_perform_add_capability(self):
        self.capability_engine\
            .perform_add_capability(data='[{"capability": "test capability", "capability_type": "test capability type"}]')
        self.assertTrue(self.capability_repository.add.called)

    def test_perform_add_capability_bad_input(self):
        self.capability_engine\
            .perform_add_capability(data='[{"capability": "test capability"}]')
        self.assertFalse(self.capability_repository.add.called)

    def test_perform_remove_capability(self):
        self.capability_engine \
            .perform_remove_capability(data='[{"capability": "test capability", "capability_type": "test capability type"}]')
        self.assertTrue(self.capability_repository.remove.called)

    def test_perform_remove_capability_bad_input(self):
        self.capability_engine \
            .perform_remove_capability(data='[{"capability": "test capability"}]')
        self.assertFalse(self.capability_repository.remove.called)


if __name__ == '__main__':
    unittest.main()

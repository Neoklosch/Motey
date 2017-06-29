import unittest
from unittest import mock

from motey.capabilityengine.capability_engine import CapabilityEngine
from motey.models.capability import Capability


class TestCapabilityEngine(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.logger = mock.patch("motey.utils.logger.Logger")
        self.capability_repository = mock.patch("motey.repositories.capability_repository.CapabilityRepository")
        self.communication_manager = mock.patch("motey.communication.communication_manager.CommunicationManager")
        self.capability_engine = CapabilityEngine(self.logger, self.capability_repository, self.communication_manager)

    def assertCapabilityEqual(self, left, right):
        for left_entry, right_entry in zip(left, right):
            if left_entry.capability != right_entry.capability:
                raise AssertionError("capability don't match")
            if left_entry.capability_type != right_entry.capability_type:
                raise AssertionError("capability type don't match")

    def test_start(self):
        pass
        # self.capability_engine.start()

    def test_stop(self):
        # self.capability_engine.stop()
        #
        # self.assertTrue(self.logger.called)
        pass

    def test_handle_capabilities_request(self):
        # self.capability_engine.handle_capabilities_request(None)
        #
        #
        # self.assertTrue(self.capability_repository.called)
        pass

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
            .perform_add_capability('[{"capability": "test capability", "capability_type": "test capability type"}]')

    def test_perform_remove_capability(self):
        pass


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest import mock

from motey.communication.apiserver import APIServer
from motey.communication.communication_manager import CommunicationManager
from motey.communication.mqttserver import MQTTServer
from motey.communication.zeromq_server import ZeroMQServer
from motey.models.image import Image


class TestCommunicationManager(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.api_server = mock.Mock(APIServer)
        self.mqtt_server = mock.Mock(MQTTServer)
        self.zeromq_server = mock.Mock(ZeroMQServer)
        self.zeromq_server.deploy_image = mock.MagicMock(return_value='abc123')
        self.zeromq_server.request_image_status = mock.MagicMock(return_value=2)
        self.zeromq_server.request_capabilities = mock.MagicMock(
            return_value={'capability': 'test capability', 'capability_type': 'test capability type'})
        self.communication_manager = CommunicationManager(api_server=self.api_server,
                                                          mqtt_server=self.mqtt_server,
                                                          zeromq_server=self.zeromq_server)
        self.test_image = Image(name='test image', engine='test engine')

    def test_start(self):
        self.communication_manager.start()

        self.assertTrue(self.api_server.start.called)
        self.assertTrue(self.mqtt_server.start.called)
        self.assertTrue(self.zeromq_server.start.called)

    def test_stop(self):
        self.communication_manager.stop()

        self.assertTrue(self.api_server.stop.called)
        self.assertTrue(self.mqtt_server.remove_node.called)
        self.assertTrue(self.mqtt_server.stop.called)
        self.assertTrue(self.zeromq_server.stop.called)

    def test_deploy_image(self):
        result = self.communication_manager.deploy_image(image=self.test_image)

        self.assertTrue(self.zeromq_server.deploy_image.called)
        self.assertEqual(result, 'abc123')

    def test_request_image_status(self):
        result = self.communication_manager.request_image_status(image=self.test_image)

        self.assertTrue(self.zeromq_server.request_image_status.called)
        self.assertEqual(result, 2)

    def test_request_capabilities(self):
        result = self.communication_manager.request_capabilities(ip='127.0.0.1')

        self.assertTrue(self.zeromq_server.request_capabilities.called)
        self.assertEqual(result['capability'], 'test capability')
        self.assertEqual(result['capability_type'], 'test capability type')

    def test_terminate_image(self):
        self.communication_manager.terminate_image(image=self.test_image)

        self.assertTrue(self.zeromq_server.terminate_image.called)


if __name__ == '__main__':
    unittest.main()

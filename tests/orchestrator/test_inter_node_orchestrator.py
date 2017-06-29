import unittest
from unittest import mock

from rx.subjects import Subject

from motey.communication.communication_manager import CommunicationManager
from motey.models.image import Image
from motey.models.image_state import ImageState
from motey.models.service import Service
from motey.models.service_state import ServiceState
from motey.orchestrator import inter_node_orchestrator
from motey.repositories.capability_repository import CapabilityRepository
from motey.repositories.nodes_repository import NodesRepository
from motey.repositories.service_repository import ServiceRepository
from motey.utils.logger import Logger
from motey.val.valmanager import VALManager


class TestInterNodeOrchestrator(unittest.TestCase):
    @classmethod
    def setUp(self):
        inter_node_orchestrator.ServiceEndpoint = mock.Mock(inter_node_orchestrator.ServiceEndpoint)
        inter_node_orchestrator.get_own_ip = mock.MagicMock(return_value='127.0.0.42')

        self.test_image = Image(name='test image name', engine='test engine', capabilities=['first', 'second', 'third'])
        self.test_service = Service(service_name='test service name', images=[self.test_image])

        self.logger = mock.Mock(Logger)
        self.valmanager = mock.Mock(VALManager)
        self.service_repository = mock.Mock(ServiceRepository)
        self.capability_repository = mock.Mock(CapabilityRepository)
        self.node_repository = mock.Mock(NodesRepository)
        self.communication_manager = mock.Mock(CommunicationManager)

        self.inter_node_orchestrator = inter_node_orchestrator.InterNodeOrchestrator(
            logger=self.logger,
            valmanager=self.valmanager,
            service_repository=self.service_repository,
            capability_repository=self.capability_repository,
            node_repository=self.node_repository,
            communication_manager=self.communication_manager
        )

        self.inter_node_orchestrator.yaml_post_stream = mock.Mock(Subject)
        self.inter_node_orchestrator.yaml_delete_stream = mock.Mock(Subject)

    def test_instantiate_service_without_image_capabilities(self):
        test_image = Image(name='test image name', engine='test engine')
        test_service = Service(service_name='test service name', images=[test_image])

        self.inter_node_orchestrator.instantiate_service(service=test_service)

        self.assertTrue(self.service_repository.add.called)
        self.assertTrue(self.service_repository.update.called)
        self.assertTrue(self.communication_manager.deploy_image.called)

    def test_instantiate_service_capabilities_equal(self):
        self.capability_repository.has = mock.MagicMock(return_value=True)

        self.inter_node_orchestrator.instantiate_service(service=self.test_service)

        self.assertTrue(self.service_repository.add.called)
        self.assertTrue(self.capability_repository.has.called)
        self.assertTrue(self.service_repository.update.called)
        self.assertTrue(self.communication_manager.deploy_image.called)

    def test_instantiate_service_capabilities_unequal_but_external_node(self):
        self.capability_repository.has = mock.MagicMock(return_value=False)
        test_node = {'ip': '127.0.0.23'}
        self.node_repository.all = mock.MagicMock(return_value=[test_node])
        self.communication_manager.request_capabilities = mock.MagicMock(
            return_value=[{'capability': 'first'}, {'capability': 'second'}, {'capability': 'third'}])

        self.inter_node_orchestrator.instantiate_service(service=self.test_service)

        self.assertTrue(self.service_repository.add.called)
        self.assertTrue(self.capability_repository.has.called)
        self.assertTrue(self.service_repository.update.called)
        self.assertTrue(self.communication_manager.deploy_image.called)

    def test_instantiate_service_capabilities_unequal_no_external_node(self):
        self.capability_repository.has = mock.MagicMock(return_value=False)
        test_node = {'ip': '127.0.0.23'}
        self.node_repository.all = mock.MagicMock(return_value=[test_node])
        self.communication_manager.request_capabilities = mock.MagicMock(
            return_value=[{'capability': 'wrong'}, {'capability': 'also wrong'}])

        self.inter_node_orchestrator.instantiate_service(service=self.test_service)

        self.assertTrue(self.service_repository.add.called)
        self.assertTrue(self.capability_repository.has.called)
        self.assertTrue(self.service_repository.update.called)
        self.assertFalse(self.communication_manager.deploy_image.called)

    def test_deploy_service(self):
        self.communication_manager.deploy_image = mock.MagicMock(return_value='abc123')
        self.service_repository.update = mock.MagicMock(return_value=None)

        self.inter_node_orchestrator.deploy_service(service=self.test_service)

        self.assertTrue(self.communication_manager.deploy_image.called)
        self.assertTrue(self.service_repository.update.called)

    def test_get_service_status_state_error(self):
        self.communication_manager.request_image_status = mock.MagicMock(return_value=ImageState.ERROR)

        result = self.inter_node_orchestrator.get_service_status(service=self.test_service)

        self.assertEqual(result, ServiceState.ERROR)
        self.assertTrue(self.communication_manager.request_image_status.called)
        self.assertTrue(self.communication_manager.terminate_image.called)
        self.assertTrue(self.service_repository.update.called)

    def test_get_service_status_state_terminated(self):
        self.communication_manager.request_image_status = mock.MagicMock(return_value=ImageState.TERMINATED)

        result = self.inter_node_orchestrator.get_service_status(service=self.test_service)

        self.assertEqual(result, ServiceState.TERMINATED)
        self.assertTrue(self.communication_manager.request_image_status.called)
        self.assertTrue(self.communication_manager.terminate_image.called)
        self.assertTrue(self.service_repository.update.called)

    def test_get_service_status_state_stopping(self):
        self.communication_manager.request_image_status = mock.MagicMock(return_value=ImageState.STOPPING)

        result = self.inter_node_orchestrator.get_service_status(service=self.test_service)

        self.assertEqual(result, ServiceState.STOPPING)
        self.assertTrue(self.communication_manager.request_image_status.called)
        self.assertTrue(self.communication_manager.terminate_image.called)
        self.assertTrue(self.service_repository.update.called)

    def test_get_service_status_state_instantiating(self):
        self.communication_manager.request_image_status = mock.MagicMock(return_value=ImageState.INSTANTIATING)

        result = self.inter_node_orchestrator.get_service_status(service=self.test_service)

        self.assertEqual(result, ServiceState.INSTANTIATING)
        self.assertTrue(self.communication_manager.request_image_status.called)
        self.assertTrue(self.service_repository.update.called)

    def test_get_service_status_state_initial(self):
        self.communication_manager.request_image_status = mock.MagicMock(return_value=ImageState.INITIAL)

        result = self.inter_node_orchestrator.get_service_status(service=self.test_service)

        self.assertEqual(result, ServiceState.INITIAL)
        self.assertTrue(self.communication_manager.request_image_status.called)
        self.assertTrue(self.service_repository.update.called)

    def test_get_service_status_state_running(self):
        self.communication_manager.request_image_status = mock.MagicMock(return_value=ImageState.RUNNING)

        result = self.inter_node_orchestrator.get_service_status(service=self.test_service)

        self.assertEqual(result, ServiceState.RUNNING)
        self.assertTrue(self.communication_manager.request_image_status.called)
        self.assertTrue(self.service_repository.update.called)

    def test_get_service_status_state_unkown(self):
        self.communication_manager.request_image_status = mock.MagicMock(return_value=999)

        result = self.inter_node_orchestrator.get_service_status(service=self.test_service)

        self.assertEqual(result, ServiceState.ERROR)
        self.assertTrue(self.communication_manager.request_image_status.called)
        self.assertTrue(self.service_repository.update.called)

    def test_compare_capabilities_both_equal(self):
        node_capabilities_dict = [{'capability': 'first'}, {'capability': 'second'}, {'capability': 'third'}]

        result = self.inter_node_orchestrator.compare_capabilities(
            needed_capabilities_list=self.test_image.capabilities,
            node_capabilities_dict=node_capabilities_dict)

        self.assertTrue(result)

    def test_compare_capabilities_both_unequal(self):
        node_capabilities_dict = [{'capability': 'wrong'}, {'capability': 'also wrong'}]

        result = self.inter_node_orchestrator.compare_capabilities(
            needed_capabilities_list=self.test_image.capabilities,
            node_capabilities_dict=node_capabilities_dict)

        self.assertFalse(result)

    def test_find_node_successfully(self):
        test_node = {'ip': '127.0.0.42'}
        self.node_repository.all = mock.MagicMock(return_value=[test_node])
        self.communication_manager.request_capabilities = mock.MagicMock(
            return_value=[{'capability': 'first'}, {'capability': 'second'}, {'capability': 'third'}])

        result = self.inter_node_orchestrator.find_node(image=self.test_image)

        self.assertIsNotNone(result)
        self.assertEqual(test_node['ip'], result['ip'])
        self.assertTrue(self.node_repository.all.called)
        self.assertTrue(self.communication_manager.request_capabilities.called)

    def test_find_node_unsuccessfully(self):
        test_node = {'ip': '127.0.0.42'}
        self.node_repository.all = mock.MagicMock(return_value=[test_node])
        self.communication_manager.request_capabilities = mock.MagicMock(
            return_value=[{'capability': 'wrong'}, {'capability': 'also wrong'}])

        result = self.inter_node_orchestrator.find_node(image=self.test_image)

        self.assertIsNone(result)
        self.assertTrue(self.node_repository.all.called)
        self.assertTrue(self.communication_manager.request_capabilities.called)

    def test_terminate_service_service_exist(self):
        self.service_repository.has = mock.MagicMock(return_value=True)

        self.inter_node_orchestrator.terminate_service(service=self.test_service)

        self.assertTrue(self.service_repository.has.called)
        self.assertTrue(self.service_repository.update.called)
        self.assertTrue(self.communication_manager.terminate_image.called)

    def test_terminate_service_service_does_not_exist(self):
        self.service_repository.has = mock.MagicMock(return_value=False)

        self.inter_node_orchestrator.terminate_service(service=self.test_service)

        self.assertTrue(self.service_repository.has.called)
        self.assertFalse(self.service_repository.update.called)
        self.assertFalse(self.communication_manager.terminate_image.called)
        self.assertTrue(self.logger.error.called)


if __name__ == '__main__':
    unittest.main()

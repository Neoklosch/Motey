import unittest
from unittest import mock

from rx.subjects import Subject
from yapsy import PluginManager
from yapsy.PluginInfo import PluginInfo

from motey.models.image import Image
from motey.repositories.capability_repository import CapabilityRepository
from motey.utils.logger import Logger
from motey.val.plugins.dockerVAL import DockerVAL
from motey.val.valmanager import VALManager


class TestVALManager(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.test_image = Image(name='test image', engine='test engine')
        self.logger = mock.Mock(Logger)
        self.capability_repository = mock.Mock(CapabilityRepository)
        self.plugin_manager = mock.Mock(PluginManager)

        self.docker_val = mock.Mock(DockerVAL)
        self.plugin_object = mock.Mock(PluginInfo)
        self.plugin_object.plugin_object = self.docker_val
        self.plugin_object.plugin_object.get_plugin_type = mock.MagicMock(return_value='test engine')

        self.plugin_manager.setPluginPlaces = mock.MagicMock(return_value=None)
        self.plugin_manager.collectPlugins = mock.MagicMock(return_value=None)
        self.plugin_manager.getAllPlugins = mock.MagicMock(return_value=[self.plugin_object])

        self.val_manager = VALManager(logger=self.logger,
                                      capability_repository=self.capability_repository,
                                      plugin_manager=self.plugin_manager)

        self.val_manager.plugin_stream = mock.Mock(Subject)

    def test_start(self):
        self.val_manager.start()

        self.assertTrue(self.capability_repository.remove_all_from_type.called)
        self.assertTrue(self.plugin_manager.setPluginPlaces.called)
        self.assertTrue(self.plugin_manager.collectPlugins.called)
        self.assertTrue(self.plugin_manager.getAllPlugins.called)
        self.assertTrue(self.docker_val.activate.called)
        self.assertTrue(self.capability_repository.add.called)

    def test_register_plugins(self):
        self.val_manager.register_plugins()

        self.assertTrue(self.capability_repository.remove_all_from_type.called)
        self.assertTrue(self.plugin_manager.setPluginPlaces.called)
        self.assertTrue(self.plugin_manager.collectPlugins.called)
        self.assertTrue(self.plugin_manager.getAllPlugins.called)
        self.assertTrue(self.docker_val.activate.called)
        self.assertTrue(self.capability_repository.add.called)

    def test_instantiate_engine_exists(self):
        self.plugin_object.plugin_object.start_instance = mock.MagicMock(return_value='abc123')

        result = self.val_manager.instantiate(image=self.test_image)

        self.assertEqual(result, 'abc123')
        self.assertTrue(self.plugin_manager.getAllPlugins.called)
        self.assertTrue(self.docker_val.get_plugin_type.called)
        self.assertTrue(self.docker_val.start_instance.called)

    def test_instantiate_engine_does_not_exists(self):
        self.plugin_object.plugin_object.get_plugin_type = mock.MagicMock(return_value='test engine unknown')
        self.plugin_object.plugin_object.start_instance = mock.MagicMock(return_value='abc123')

        result = self.val_manager.instantiate(image=self.test_image)

        self.assertEqual(result, None)
        self.assertTrue(self.plugin_manager.getAllPlugins.called)
        self.assertTrue(self.docker_val.get_plugin_type.called)
        self.assertFalse(self.docker_val.start_instance.called)

    def test_get_instance_state_engine_exists(self):
        self.plugin_object.plugin_object.get_image_instance_state = mock.MagicMock(return_value=2)

        result = self.val_manager.get_instance_state(image=self.test_image)

        self.assertEqual(result, 2)
        self.assertTrue(self.plugin_manager.getAllPlugins.called)
        self.assertTrue(self.docker_val.get_plugin_type.called)
        self.assertTrue(self.docker_val.get_image_instance_state.called)

    def test_get_instance_state_engine_does_not_exists(self):
        self.plugin_object.plugin_object.get_plugin_type = mock.MagicMock(return_value='test engine unknown')

        result = self.val_manager.get_instance_state(image=self.test_image)

        self.assertEqual(result, 5)
        self.assertTrue(self.plugin_manager.getAllPlugins.called)
        self.assertTrue(self.docker_val.get_plugin_type.called)
        self.assertFalse(self.docker_val.get_image_instance_state.called)

    def test_terminate_engine_exist(self):
        self.val_manager.terminate(image=self.test_image)

        self.assertTrue(self.plugin_manager.getAllPlugins.called)
        self.assertTrue(self.docker_val.get_plugin_type.called)
        self.assertTrue(self.docker_val.stop_instance.called)

    def test_terminate_engine_does_not_exist(self):
        self.plugin_object.plugin_object.get_plugin_type = mock.MagicMock(return_value='test engine unknown')

        self.val_manager.terminate(image=self.test_image)

        self.assertTrue(self.plugin_manager.getAllPlugins.called)
        self.assertTrue(self.docker_val.get_plugin_type.called)
        self.assertFalse(self.docker_val.stop_instance.called)

    def test_close(self):
        self.val_manager.close()

        self.assertTrue(self.plugin_manager.getAllPlugins.called)
        self.assertTrue(self.capability_repository.remove.called)
        self.assertTrue(self.docker_val.deactivate.called)


if __name__ == '__main__':
    unittest.main()

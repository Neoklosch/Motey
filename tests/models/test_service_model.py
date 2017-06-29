import unittest
import uuid

from motey.models.image import Image
from motey.models.service import Service
from motey.models.service_state import ServiceState


class TestServiceModel(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.service_id = uuid.uuid4().hex
        self.expecting_service = Service(id=self.service_id,
                                         service_name='test name',
                                         state=ServiceState.RUNNING,
                                         images=[Image(name='test image', engine=('test engine')), ],
                                         state_message='test state message')

    def test_service_construction(self):
        resulting_service = Service(id=self.service_id,
                                    service_name='test name',
                                    state=ServiceState.RUNNING,
                                    images=[Image(name='test image', engine=('test engine')), ],
                                    state_message='test state message')
        self.assertTrue(resulting_service.id == self.service_id and
                        resulting_service.service_name == 'test name' and
                        resulting_service.state == ServiceState.RUNNING and
                        resulting_service.images[0].name == 'test image' and
                        resulting_service.images[0].engine == 'test engine' and
                        resulting_service.state_message == 'test state message')

    def test_dict_to_service(self):
        resulting_service = Service.transform(data={
            'id': self.service_id,
            'service_name': 'test name',
            'state': ServiceState.RUNNING,
            'images': [{'name': 'test image', 'engine': 'test engine'}, ],
            'state_message': 'test state message'
        })
        self.assertTrue(resulting_service.id == self.expecting_service.id and
                        resulting_service.service_name == self.expecting_service.service_name and
                        resulting_service.state == self.expecting_service.state and
                        resulting_service.images[0].name == 'test image' and
                        resulting_service.images[0].engine == 'test engine' and
                        resulting_service.state_message == self.expecting_service.state_message)

    def test_dict_to_none(self):
        resulting_service = Service.transform(data={'service_name': 'test service name'})
        self.assertEqual(resulting_service, None)

        resulting_service = Service.transform(data={'images': 'test images'})
        self.assertEqual(resulting_service, None)

    def test_service_to_dict(self):
        test_dict = {
            'id': self.service_id,
            'service_name': 'test name',
            'state': ServiceState.RUNNING,
            'images': [{'id': '',
                        'name': 'test image',
                        'engine': 'test engine',
                        'node': None,
                        'capabilities': {},
                        'parameters': {}}, ],
            'state_message': 'test state message'
        }
        resulting_dict = dict(self.expecting_service)
        self.assertTrue(resulting_dict['id'] == test_dict['id'] and
                        resulting_dict['service_name'] == test_dict['service_name'] and
                        resulting_dict['state'] == test_dict['state'] and
                        resulting_dict['images'] == test_dict['images'] and
                        resulting_dict['state_message'] == test_dict['state_message'])

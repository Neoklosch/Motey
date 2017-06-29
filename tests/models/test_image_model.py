import unittest

from motey.models.image import Image


class TestImageModel(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.test_dict = {
            'id': 'abc123',
            'name': 'test name',
            'engine': 'test engine',
            'parameters': {'testparam': 'test param value'},
            'capabilities': {'capability': 'test capability', 'capability_type': 'test capability type'},
            'node': {'ip': '127.0.0.42'}
        }
        self.expecting_image = Image(id='abc123',
                                     name='test name',
                                     engine='test engine',
                                     parameters={'testparam': 'test param value'},
                                     capabilities={'capability': 'test capability',
                                                   'capability_type': 'test capability type'},
                                     node={'ip': '127.0.0.42'})

    def test_image_construction(self):
        resulting_image = Image(id='abc123',
                                name='test name',
                                engine='test engine',
                                parameters={'testparam': 'test param value'},
                                capabilities={'capability': 'test capability',
                                              'capability_type': 'test capability type'},
                                node={'ip': '127.0.0.42'})
        self.assertTrue(resulting_image.id == 'abc123' and
                        resulting_image.name == 'test name' and
                        resulting_image.engine == 'test engine' and
                        resulting_image.parameters == {'testparam': 'test param value'} and
                        resulting_image.capabilities == {'capability': 'test capability',
                                                         'capability_type': 'test capability type'} and
                        resulting_image.node == {'ip': '127.0.0.42'})

    def test_dict_to_image(self):
        resulting_image = Image.transform(data=self.test_dict)
        self.assertTrue(resulting_image.id == self.expecting_image.id and
                        resulting_image.name == self.expecting_image.name and
                        resulting_image.engine == self.expecting_image.engine and
                        resulting_image.parameters == self.expecting_image.parameters and
                        resulting_image.capabilities == self.expecting_image.capabilities and
                        resulting_image.node == self.expecting_image.node)

    def test_dict_to_none(self):
        resulting_image = Image.transform(data={'name': 'test name'})
        self.assertEqual(resulting_image, None)

        resulting_image = Image.transform(data={'engine': 'test engine'})
        self.assertEqual(resulting_image, None)

    def test_image_to_dict(self):
        resulting_dict = dict(self.expecting_image)
        self.assertTrue(resulting_dict['id'] == self.test_dict['id'] and
                        resulting_dict['name'] == self.test_dict['name'] and
                        resulting_dict['engine'] == self.test_dict['engine'] and
                        resulting_dict['parameters'] == self.test_dict['parameters'] and
                        resulting_dict['capabilities'] == self.test_dict['capabilities'] and
                        resulting_dict['node'] == self.test_dict['node'])

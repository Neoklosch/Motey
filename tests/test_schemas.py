import unittest

from jsonschema import validate

from motey.models.schemas import blueprint_yaml_schema


class TestSchemas(unittest.TestCase):

    @classmethod
    def setUp(self):
        pass

    def test_blueprint_schema(self):
        data = {
            'service_name': 'test_service_name',
            'node_type': 'MASTER',
            'images': [
                {
                    'name': 'test_image_name',
                    'engine': 'docker',
                    'parameters': {
                        'ports': {
                            'tcp/80': 8080,
                            'detach': True,
                            'name': 'motey_test_image'
                        }
                    },
                    'capabilities': [
                        'docker', 'zigbee', 'wifi'
                    ]
                },
                {
                    'name': 'second_test_image_name',
                    'engine': 'docker',
                    'parameters': {
                        'ports': {
                            'tcp/9000': 9001,
                            'detach': False,
                            'name': 'motey_second_test_image'
                        }
                    }
                },
                {
                    'name': 'third_test_image_name',
                    'engine': 'XEN'
                }
            ]
        }
        validate(data, blueprint_yaml_schema)


if __name__ == '__main__':
    unittest.main()

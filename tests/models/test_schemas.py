import unittest

from jsonschema import validate

from motey.models.schemas import blueprint_yaml_schema
from motey.models.schemas import capability_json_schema
from jsonschema import ValidationError


class TestSchemas(unittest.TestCase):
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
        self.assertEqual(validate(data, blueprint_yaml_schema), None)

    def test_blueprint_schema_error(self):
        data = {
            'service_name': 'test_service_name'
        }
        with self.assertRaises(ValidationError) as cm:
            validate(data, blueprint_yaml_schema)

    def test_capability_json_schema(self):
        data = [{
            "capability": 'test capability',
            "capability_type": 'test capability type'
        }]
        self.assertEqual(validate(data, capability_json_schema), None)

    def test_capability_json_schema_error(self):
        data = [{
            "capability_type": 'test capability type'
        }]
        with self.assertRaises(ValidationError) as cm:
            validate(data, capability_json_schema)

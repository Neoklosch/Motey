import yaml
from jsonschema import validate


class ValidationError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


schema = {
    "type": "object",
    "properties": {
        "images": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "image_name": {
                        "type": "string"
                    },
                    "parameters": {
                        "type": "object"
                    },
                    "capabilities": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": ["image_name"]
            }
        }
    }
}

good_instance = """
---
images:
- image_name: alpine
  parameters:
    ports:
      80/tcp: 8080
      7070/udp: 9001
    name: motey_alpine
- image_name: busybox
  parameters:
    ports:
      80/tcp: 8080
    name: busybox_test_container
  capabilities:
    - docker
- image_name: keks
  parameters:
    ports:
      80/tcp: 8080
    name: busybox_test_container
  capabilities:
    - docker
- image_name: nginx
  parameters:
    ports:
      80/tcp: 8080
    detach: true
    name: nginx_from_motey
  capabilities:
    - docker
"""


result = yaml.load(good_instance)
print(result)
validate(result, schema)

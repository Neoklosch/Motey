# Schema to validate a yaml blueprint
blueprint_yaml_schema = {
    "type": "object",
    "properties": {
        "service_name": {
            "type": "string"
        },
        "action": {
            "type": "string"
        },
        "node_type": {
            "type": "string"
        },
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
                        },
                        "minItems": 1,
                        "uniqueItems": True,
                    }
                },
                "required": ["image_name"]
            },
            "minItems": 1,
            "uniqueItems": True
        }
    },
    "required": ["service_name", "images", "action"]
}

# The schema to validate capability json data.
capability_json_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "label": {
                "type": "string"
            },
            "label_type": {
                "type": "string"
            }
        },
        "required": ["label", "label_type"]
    }
}

# JSON schema for a valid label entry
label_json_schema = {
    "type": "object",
    "properties": {
        "label": {
            "type": "string"
        },
        "label_type": {
            "type": "string"
        },
        "action": {
            "enum": ["add", "remove"]
        }
    },
    "required": ["label", "label_type", "action"]
}

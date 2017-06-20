# Schema to validate a yaml blueprint
blueprint_yaml_schema = {
    "type": "object",
    "properties": {
        "service_name": {
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
                    "name": {
                        "type": "string"
                    },
                    "engine": {
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
                "required": ["name", "engine"]
            },
            "minItems": 1,
            "uniqueItems": True
        }
    },
    "required": ["service_name", "images"]
}

# The schema to validate capability json data.
capability_json_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "capability": {
                "type": "string"
            },
            "capability_type": {
                "type": "string"
            }
        },
        "required": ["capability", "capability_type"]
    }
}

# JSON schema for a valid capability entry
capability_action_json_schema = {
    "type": "object",
    "properties": {
        "capability": {
            "type": "string"
        },
        "capability_type": {
            "type": "string"
        },
        "action": {
            "enum": ["add", "remove"]
        }
    },
    "required": ["capability", "capability_type", "action"]
}

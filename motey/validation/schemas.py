# Schema to validate a yaml blueprint
blueprint_schema = {
    "type": "object",
    "properties": {
        "service_name": {
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
    "required": ["service_name", "images"]
}

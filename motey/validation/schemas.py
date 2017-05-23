# Schema to validate a yaml blueprint
blueprint_schema = {
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

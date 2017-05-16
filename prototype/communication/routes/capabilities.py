import json
from json import JSONDecodeError
from flask import jsonify, request, abort
from flask.views import MethodView
from rx.subjects import Subject
from prototype.labeling.labelingengine import LabelingEngine
from jsonschema import validate, ValidationError


class Capabilities(MethodView):
    stream = Subject()
    json_schema = {
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

    def get(self):
        labeling_engine = LabelingEngine.Instance()
        results = labeling_engine.get_all_labels()
        return jsonify(results), 200

    def put(self):
        if request.content_type == 'application/json':
            data = request.json
            try:
                validate(data, self.json_schema)
                labeling_engine = LabelingEngine.Instance()
                nothing_added = True
                for entry in data:
                    if not labeling_engine.has_label(label=entry['label']):
                        nothing_added = False
                        labeling_engine.add_label(label=entry['label'], label_type=entry['label_type'])
                if nothing_added:
                    return '', 304
            except ValidationError:
                return 'Validation Error', 400
        else:
            return 'Wrong Content type', 400
        return '', 201

    def delete(self):
        if request.content_type == 'application/json':
            data = request.json
            try:
                validate(data, self.json_schema)
                labeling_engine = LabelingEngine.Instance()
                nothing_removed = True
                for entry in data:
                    if labeling_engine.has_label(label=entry['label']):
                        nothing_removed = False
                        labeling_engine.remove_label(label=entry['label'], label_type=entry['label_type'])
                if nothing_removed:
                    return '', 304
            except ValidationError:
                return 'Validation Error', 400
        else:
            return 'Wrong Content type', 400
        return '', 201

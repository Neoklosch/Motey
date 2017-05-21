import yaml
from flask import request, abort
from flask.views import MethodView
from jsonschema import validate, ValidationError
from rx.subjects import Subject

from motey.validation.schemas import blueprint_schema


class BlueprintEndpoint(MethodView):
    stream = Subject()

    def post(self):
        if request.content_type == 'application/x-yaml':
            result = request.get_data(cache=False, as_text=True)
            try:
                loaded_data = yaml.load(result)
                validate(loaded_data, blueprint_schema)
                self.stream.on_next(result)
            except (yaml.YAMLError, ValidationError):
                return abort(400)
            return '', 201
        else:
            return abort(400)

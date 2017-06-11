import yaml
from flask import request, abort
from flask.views import MethodView
from jsonschema import validate, ValidationError
from rx.subjects import Subject

from motey.models.schemas import blueprint_yaml_schema


class BlueprintEndpoint(MethodView):
    """
    This REST API endpoint let the client upload an YAML file to the node.
    """

    # RX subject which send a message, after a POST is received and successfully parsed.
    yaml_post_stream = Subject()

    def post(self):
        """
        POST endpoint.
        Receive the YAMl file and validates them.
        The content type of the request must be ``application/x-yaml``, otherwiese the request will end up in a HTTP
        status code 400 - Bad Request.

        :return: HTTP status code 201 - Created, if the request is successful, otherwise 400 - Bad Request.
        """
        if request.content_type == 'application/x-yaml':
            result = request.get_data(cache=False, as_text=True)
            try:
                loaded_data = yaml.load(result)
                validate(loaded_data, blueprint_yaml_schema)
                self.yaml_post_stream.on_next(result)
            except (yaml.YAMLError, ValidationError):
                return abort(400)
            return '', 201
        else:
            return abort(400)

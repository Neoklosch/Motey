import yaml
from flask import jsonify
from flask import request, abort
from flask.views import MethodView
from jsonschema import validate, ValidationError
from rx.subjects import Subject

from motey.models.schemas import blueprint_yaml_schema


class Service(MethodView):
    """
    This REST API endpoint for getting service informations and also let the client upload a YAML file to the node.
    A service contain all the running images.
    """

    # RX subject which send a message, after a POST is received and successfully parsed.
    yaml_post_stream = Subject()

    def get(self):
        """
        Returns a list off all existing capabilities of this node.

        :return: a JSON object with all the existing capabilities of this node
        """
        from motey.di.app_module import DIRepositories
        results = DIRepositories.service_repository().all()
        return jsonify(results), 200

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

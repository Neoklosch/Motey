from flask import jsonify, request
from flask.views import MethodView
from jsonschema import validate, ValidationError


class Capabilities(MethodView):
    """
    This REST API endpoint for capability handling.
    A capability is basically a label for the whole node.
    New capabilities can be added or deleted via this endpoint or a list with the existing ones can be fetched.
    """

    # The schema to validate the sent json data.
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
        """
        Returns a list off all existing capabilities of this node.

        :return: a JSON object with all the existing capabilities of this node
        """
        from motey.di.app_module import DIRepositories
        results = DIRepositories.labeling_repository().all()
        return jsonify(results), 200

    def put(self):
        """
        Add a list of new capabilities or at least a single one to the node.
        The content type of the request must be ``application/json``, otherwise the request will fail.

        :return: 201 - Created if at least one capability was added, 304 - Not Modified if non of the sent capabilities
         was added or 400 - Bad Request if the wrong content type was sent or the json does not match the
         ``json_schema``.
        """
        from motey.di.app_module import DIRepositories
        if request.content_type == 'application/json':
            data = request.json
            try:
                validate(data, self.json_schema)
                labeling_repository = DIRepositories.labeling_repository()
                nothing_added = True
                for entry in data:
                    if not labeling_repository.has_node(label=entry['label']):
                        nothing_added = False
                        labeling_repository.add(label=entry['label'], label_type=entry['label_type'])
                if nothing_added:
                    return '', 304
            except ValidationError:
                return 'Validation Error', 400
        else:
            return 'Wrong Content type', 400
        return '', 201

    def delete(self):
        """
        Remove a list of capabilities or at least a single one from the node.
        The content type of the request must be ``application/json``, otherwise the request will fail.

        :return: 201 - Created if at least one capability was removed, 304 - Not Modified if non of the sent
                 capabilities was removed because they don not exists or 400 - Bad Request if the wrong content type was sent or
                 the json does not match the ``json_schema``.
        """
        from motey.di.app_module import DIRepositories
        if request.content_type == 'application/json':
            data = request.json
            try:
                validate(data, self.json_schema)
                labeling_repository = DIRepositories.labeling_repository()
                nothing_removed = True
                for entry in data:
                    if labeling_repository.has_node(label=entry['label']):
                        nothing_removed = False
                        labeling_repository.remove(label=entry['label'], label_type=entry['label_type'])
                if nothing_removed:
                    return '', 304
            except ValidationError:
                return 'Validation Error', 400
        else:
            return 'Wrong Content type', 400
        return '', 201

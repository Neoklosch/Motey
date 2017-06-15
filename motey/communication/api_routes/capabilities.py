from flask import jsonify, request
from flask.views import MethodView
from jsonschema import validate, ValidationError

from motey.models.schemas import capability_json_schema


class Capabilities(MethodView):
    """
    This REST API endpoint for capability handling.
    A capability is basically a capability for the whole node.
    New capabilities can be added or deleted via this endpoint or a list with the existing ones can be fetched.
    """

    def get(self):
        """
        Returns a list off all existing capabilities of this node.

        :return: a JSON object with all the existing capabilities of this node
        """
        from motey.di.app_module import DIRepositories
        results = DIRepositories.capability_repository().all()
        return jsonify(results), 200

    def put(self):
        """
        Add a list of new capabilities or at least a single one to the node.
        The content type of the request must be ``application/json``, otherwise the request will fail.

        :return: 201 - Created if at least one capability was added, 304 - Not Modified if non of the sent capabilities
                 was added or 400 - Bad Request if the wrong content type was sent or the json does not match the
                 ``motey.models.schemas.capability_schema``.
        """
        from motey.di.app_module import DIRepositories
        if request.content_type == 'application/json':
            data = request.json
            try:
                validate(data, capability_json_schema)
                capability_repository = DIRepositories.capability_repository()
                nothing_added = True
                for entry in data:
                    if not capability_repository.has_node(capability=entry['capability']):
                        nothing_added = False
                        capability_repository.add(capability=entry['capability'],
                                                  capability_type=entry['capability_type'])
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
                 the json does not match the ``motey.models.schemas.capability_schema``.
        """
        from motey.di.app_module import DIRepositories
        if request.content_type == 'application/json':
            data = request.json
            try:
                validate(data, capability_json_schema)
                capability_repository = DIRepositories.capability_repository()
                nothing_removed = True
                for entry in data:
                    if capability_repository.has_node(capability=entry['capability']):
                        nothing_removed = False
                        capability_repository.remove(capability=entry['capability'],
                                                     capability_type=entry['capability_type'])
                if nothing_removed:
                    return '', 304
            except ValidationError:
                return 'Validation Error', 400
        else:
            return 'Wrong Content type', 400
        return '', 201

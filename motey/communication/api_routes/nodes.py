from flask import jsonify
from flask.views import MethodView
from rx.subjects import Subject


class Nodes(MethodView):
    """
    This REST API endpoint for getting all registered nodes.
    """

    # RX subject which send a message, after a POST is received and successfully parsed.
    yaml_post_stream = Subject()

    def get(self):
        """
        Returns a list off all registered nodes.

        :return: a JSON object with all registered nodes
        """
        from motey.di.app_module import DIRepositories
        results = DIRepositories.nodes_repository().all()
        return jsonify(results), 200

from flask import Blueprint, abort

# Represents a ``Flask`` ``Blueprint```which adds an heartbeat REST API endpoint
heartbeat = Blueprint('heartbeat', __name__)

# List with all the registered callbacks for the heartbeat endpoint
callbacks = []


@heartbeat.route('/v1/heartbeat')
def check_heartbeat():
    """
    The endpoint himself.
    Will be executed if the url is requested.

    :return: 204 - No Content, if the node is up and running and all the registered callbacks requirements are
    fulfilled, otherwise 400 - Bad Request.
    """
    if not all(callback() for callback in callbacks):
        return abort(400)

    return '', 204


def register_callback(callback):
    """
    Helper method to register a new callback.

    :param callback: callback to be added to the queue
    """
    callbacks.append(callback)


def register_heartbeat(flask_app):
    """
    Helper method to register the heartbeat to the ``Flask`` webserver.
    Does not works with other webservers.

    :param flask_app: the ``Flask`` instance.
    """
    flask_app.register_blueprint(heartbeat)

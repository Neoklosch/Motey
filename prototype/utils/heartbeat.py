import logging
from flask import Blueprint, abort

heartbeat = Blueprint('heartbeat', __name__)

callbacks = []


@heartbeat.route('/heartbeat')
def check_heartbeat():
    if not all(callback() for callback in callbacks):
        return abort(500)

    return ('', 204)


def register_callback(callback):
    callbacks.append(callback)


def register_heartbeat(flask_app):
    flask_app.register_blueprint(heartbeat)


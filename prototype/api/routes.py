from flask import Blueprint


routes = Blueprint('routes', __name__, template_folder='api/templates')


@routes.route('/second')
def second():
    return "second works also"

@routes.route('/third')
def third():
    return "you know"
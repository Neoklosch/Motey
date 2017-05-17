from flask import request, abort
from flask.views import MethodView
from rx.subjects import Subject


class BlueprintEndpoint(MethodView):
    stream = Subject()

    def post(self):
        if request.content_type == 'application/x-yaml':
            result = request.get_data(cache=False, as_text=True)
            self.stream.on_next(result)
            return '', 201
        else:
            return abort(400)

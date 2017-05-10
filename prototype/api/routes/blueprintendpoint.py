from flask import request
from flask.views import MethodView
from rx.subjects import Subject


class BlueprintEndpoint(MethodView):
    stream = Subject()

    def post(self):
        if request.content_type == 'application/x-yaml':
            result = request.get_data(cache=False, as_text=True)
            print(result)
            self.stream.on_next(result)
            return 'done', 201
        else:
            return 400
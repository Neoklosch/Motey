from flask import request
from flask_restful import Resource, reqparse
from rx.subjects import Subject


class BlueprintEndpoint(Resource):
    stream = Subject()

    def __init__(self):
        self.parser = reqparse.RequestParser()

    def post(self):
        if request.content_type == 'application/x-yaml':
            result = request.get_data(cache=False, as_text=True)
            print(result)
            self.stream.on_next(result)
            return 'done', 201
        else:
            return 400
from flask import jsonify
from flask.views import MethodView
from rx.subjects import Subject
from prototype.labeling.labelingengine import LabelingEngine


class NodeStatus(MethodView):
    stream = Subject()

    def get(self):
        labeling_engine = LabelingEngine.Instance()
        results = labeling_engine.get_all_labels()
        return jsonify(results), 200
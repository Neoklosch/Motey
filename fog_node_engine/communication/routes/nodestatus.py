from flask import jsonify
from flask.views import MethodView
from rx.subjects import Subject
from fog_node_engine.labeling.labelingengine import LabelingEngine
import psutil


class NodeStatus(MethodView):
    stream = Subject()

    def get(self):
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        status = {
            'cpu': self.get_average_cpu(),
            'memory': {
                'total': memory.total,
                'available': memory.available,
                'percent': memory.percent,
                'used': memory.used,
                'free': memory.free,
            },
            'disk': {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent,
            }
        }
        return jsonify(status), 200

    def get_average_cpu(self, loops=5):
        cpu = 0
        for x in range(loops):
            cpu += psutil.cpu_percent(interval=1)
        return (cpu / loops)

import psutil
from flask import jsonify
from flask.views import MethodView


class NodeStatus(MethodView):
    """
    Give information about the current hardware usage of the node.
    This includes the cpu, memory and disk usage.
    """

    def get(self):
        """
        Returns the currant hardware usage of the node.

        :return: a json object with the current hardware usage of the node.
        """
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
        """
        Helper method to get an average cpu usage.

        :param loops: the number of iterations to sum up the avarage cpu usage.
        :return: The avarage cpu usage as a float.
        """
        cpu = 0
        for x in range(loops):
            cpu += psutil.cpu_percent(interval=1)
        return cpu / loops

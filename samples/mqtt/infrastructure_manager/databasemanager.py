import os

from decorators.singleton import Singleton
from tinydb import TinyDB, Query


@Singleton
class DatabaseManager(object):
    def __init__(self):
        self.db = TinyDB(os.path.abspath('infrastructure_manager/repositories/nodes.json'))

    def get_all_nodes(self):
        return self.db.all()

    def add_node(self, ip):
        if not self.has_node(ip):
            self.db.insert({'node': ip})

    def remove_node(self, ip):
        self.db.remove(Query().node == ip)

    def clear(self):
        self.db.remove()

    def has_node(self, ip):
        return len(self.db.search(Query().node == ip)) > 0

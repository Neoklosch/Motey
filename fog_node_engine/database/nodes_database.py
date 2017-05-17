import os
from tinydb import TinyDB, Query
from fog_node_engine.decorators.singleton import Singleton
from fog_node_engine.configuration.configreader import config


@Singleton
class NodesDatabase(object):
    def __init__(self):
        self.db = TinyDB(os.path.abspath('%s/nodes.json' % config['DATABASE']['path']))

    def all(self):
        return self.db.all()

    def add(self, ip):
        if not self.has(ip):
            self.db.insert({'ip': ip})

    def remove(self, ip):
        self.db.remove(Query().ip == ip)

    def clear(self):
        self.db.remove()

    def has(self, ip):
        return len(self.db.search(Query().ip == ip)) > 0

import os

from tinydb import TinyDB, Query

from motey.configuration.configreader import config
from motey.decorators.singleton import Singleton


@Singleton
class NodesRepository(object):
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

import unittest
from unittest import mock

from tinydb import TinyDB, Query

from motey.repositories import nodes_repository


class TestNodeRepository(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.test_ip = '127.0.0.42'
        nodes_repository.config = {'DATABASE': {'path': '/tmp/testpath'}}
        nodes_repository.BaseRepository = mock.Mock(nodes_repository.BaseRepository)
        nodes_repository.TinyDB = mock.Mock(TinyDB)
        nodes_repository.Query = mock.Mock(Query)
        self.test_node_repository = nodes_repository.NodesRepository()

    def test_construction(self):
        self.assertIsNotNone(self.test_node_repository.db)

    def test_add_ip_does_not_exist(self):
        self.test_node_repository.has = mock.MagicMock(return_value=False)
        self.test_node_repository.db.insert = mock.MagicMock(return_value='123')

        self.test_node_repository.add(self.test_ip)

        self.assertTrue(self.test_node_repository.db.insert.called)

    def test_add_ip_exist(self):
        self.test_node_repository.has = mock.MagicMock(return_value=True)
        self.test_node_repository.db.insert = mock.MagicMock(return_value='123')

        self.test_node_repository.add(self.test_ip)

        self.assertFalse(self.test_node_repository.db.insert.called)

    def test_remove(self):
        self.test_node_repository.remove(self.test_ip)

        self.assertTrue(self.test_node_repository.db.remove.called)

    def test_has_entry(self):
        self.test_node_repository.db.search = mock.MagicMock(return_value=[1, 2])

        result = self.test_node_repository.has(self.test_ip)

        self.assertTrue(self.test_node_repository.db.search.called)
        self.assertTrue(result)

    def test_has_no_entry(self):
        self.test_node_repository.db.search = mock.MagicMock(return_value=[])

        result = self.test_node_repository.has(self.test_ip)

        self.assertTrue(self.test_node_repository.db.search.called)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()

import unittest
import uuid
from unittest import mock

from tinydb import TinyDB, Query

from motey.repositories import capability_repository


class TestCapabilityRepository(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.test_capability = 'test capability'
        self.test_capability_type = 'test capability type'
        capability_repository.config = {'DATABASE': {'path': '/tmp/testpath'}}
        capability_repository.BaseRepository = mock.Mock(capability_repository.BaseRepository)
        capability_repository.TinyDB = mock.Mock(TinyDB)
        capability_repository.Query = mock.Mock(Query)
        self.test_capability_repository = capability_repository.CapabilityRepository()

    def test_construction(self):
        self.assertIsNotNone(self.test_capability_repository.db)

    def test_add_capability_does_not_exist(self):
        self.test_capability_repository.has = mock.MagicMock(return_value=False)
        self.test_capability_repository.db.insert = mock.MagicMock(return_value='123')

        self.test_capability_repository.add(capability=self.test_capability, capability_type=self.test_capability_type)

        self.assertTrue(self.test_capability_repository.db.insert.called)

    def test_add_capability_exist(self):
        self.test_capability_repository.has = mock.MagicMock(return_value=True)
        self.test_capability_repository.db.insert = mock.MagicMock(return_value='123')

        self.test_capability_repository.add(capability=self.test_capability, capability_type=self.test_capability_type)

        self.assertFalse(self.test_capability_repository.db.insert.called)

    def test_remove_without_type(self):
        self.test_capability_repository.remove(capability=self.test_capability)

        self.assertTrue(self.test_capability_repository.db.remove.called)

    def test_remove_with_type(self):
        self.test_capability_repository.remove(capability=self.test_capability, capability_type=self.test_capability_type)

        self.assertTrue(self.test_capability_repository.db.remove.called)

    def test_remove_all_from_type(self):
        self.test_capability_repository.remove_all_from_type(capability_type=self.test_capability_type)

        self.assertTrue(self.test_capability_repository.db.remove.called)

    def test_has_entry(self):
        self.test_capability_repository.db.search = mock.MagicMock(return_value=[1, 2])

        result = self.test_capability_repository.has(capability=self.test_capability)

        self.assertTrue(self.test_capability_repository.db.search.called)
        self.assertTrue(result)

    def test_has_no_entry(self):
        self.test_capability_repository.db.search = mock.MagicMock(return_value=[])

        result = self.test_capability_repository.has(capability=self.test_capability)

        self.assertTrue(self.test_capability_repository.db.search.called)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()

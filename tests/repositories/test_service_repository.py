import unittest
import uuid
from unittest import mock

from tinydb import TinyDB, Query

from motey.models.service import Service
from motey.repositories import service_repository


class TestServiceRepository(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.text_service_id = uuid.uuid4().hex
        self.test_service = {'id': self.text_service_id, 'service_name': 'test service name', 'images': ['test image']}
        service_repository.config = {'DATABASE': {'path': '/tmp/testpath'}}
        service_repository.BaseRepository = mock.Mock(service_repository.BaseRepository)
        service_repository.TinyDB = mock.Mock(TinyDB)
        service_repository.Query = mock.Mock(Query)
        self.test_service_repository = service_repository.ServiceRepository()

    def test_construction(self):
        self.assertIsNotNone(self.test_service_repository.db)

    def test_add_service_does_not_exist(self):
        self.test_service_repository.has = mock.MagicMock(return_value=False)
        self.test_service_repository.db.insert = mock.MagicMock(return_value='123')

        self.test_service_repository.add(service=self.test_service)

        self.assertTrue(self.test_service_repository.db.insert.called)

    def test_add_servie_exist(self):
        self.test_service_repository.has = mock.MagicMock(return_value=True)
        self.test_service_repository.db.insert = mock.MagicMock(return_value='123')

        self.test_service_repository.add(service=self.test_service)

        self.assertFalse(self.test_service_repository.db.insert.called)

    def test_udpate(self):
        self.test_service_repository.update(service=self.test_service)

        self.assertTrue(self.test_service_repository.db.update.called)

    def test_remove(self):
        self.test_service_repository.remove(service_id=self.test_service['id'])

        self.assertTrue(self.test_service_repository.db.remove.called)

    def test_has_entry(self):
        self.test_service_repository.db.search = mock.MagicMock(return_value=[1, 2])

        result = self.test_service_repository.has(service_id=self.test_service['id'])

        self.assertTrue(self.test_service_repository.db.search.called)
        self.assertTrue(result)

    def test_has_no_entry(self):
        self.test_service_repository.db.search = mock.MagicMock(return_value=[])

        result = self.test_service_repository.has(service_id=self.test_service['id'])

        self.assertTrue(self.test_service_repository.db.search.called)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()

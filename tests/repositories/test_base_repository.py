import unittest
from unittest import mock

from tinydb import TinyDB

from motey.repositories import base_repository


class TestBaseRepository(unittest.TestCase):
    @classmethod
    def setUp(self):
        base_repository.config = {'DATABASE': {'path': '/tmp/testpath'}}
        base_repository.os = mock.Mock(base_repository.os)
        base_repository.os.path = mock.Mock(base_repository.os.path)
        base_repository.os.makedirs = mock.MagicMock(return_value=None)
        base_repository.os.path.exists = mock.MagicMock(return_value=True)

    def test_start_folder_exist(self):
        test_base_repository = base_repository.BaseRepository()

        self.assertTrue(base_repository.os.path.exists.called)
        self.assertFalse(base_repository.os.makedirs.called)

    def test_start_folder_does_not_exist(self):
        base_repository.os.makedirs = mock.MagicMock(return_value=None)
        base_repository.os.path.exists = mock.MagicMock(return_value=False)

        test_base_repository = base_repository.BaseRepository()

        self.assertTrue(base_repository.os.path.exists.called)
        self.assertTrue(base_repository.os.makedirs.called)

    def test_start_folder_can_not_created(self):
        base_repository.os.makedirs = mock.MagicMock(return_value=OSError)
        base_repository.os.path.exists = mock.MagicMock(return_value=False, side_effect=OSError)

        with self.assertRaises(OSError) as ose:
            test_base_repository = base_repository.BaseRepository()

        self.assertTrue(base_repository.os.path.exists.called)
        self.assertFalse(base_repository.os.makedirs.called)

    def test_all_no_database(self):
        test_base_repository = base_repository.BaseRepository()

        result = test_base_repository.all()

        self.assertIsNone(result)

    def test_all_with_database(self):
        test_base_repository = base_repository.BaseRepository()
        test_base_repository.db = mock.Mock(TinyDB)
        test_base_repository.db.all = mock.MagicMock(return_value=[{'entry': 'test entry'}])

        result = test_base_repository.all()

        self.assertIsNotNone(result)

    def test_clear_with_database(self):
        test_base_repository = base_repository.BaseRepository()
        test_base_repository.db = mock.Mock(TinyDB)
        test_base_repository.db.purge = mock.MagicMock(return_value=None)

        test_base_repository.clear()

        self.assertTrue(test_base_repository.db.purge.called)


if __name__ == '__main__':
    unittest.main()

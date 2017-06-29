import os
import sys
import unittest

from motey.utils.path_helper import absolute_file_path


class TestPathHelper(unittest.TestCase):
    test_file_name = 'test_path_helper.py'

    @classmethod
    def setUp(self):
        self.expected_file_path = '%s/%s' % (os.path.dirname(sys.modules['__main__'].__file__), self.test_file_name)

    def test_absolute_file_path(self):
        resulting_file_path = absolute_file_path(self.test_file_name)
        self.assertEqual(self.expected_file_path, resulting_file_path)

    def test_absolute_file_path_with_leading_slash(self):
        resulting_file_path = absolute_file_path('/%s' % self.test_file_name)
        self.assertEqual(self.expected_file_path, resulting_file_path)

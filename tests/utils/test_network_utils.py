import socket as Socket
import unittest
from unittest.mock import MagicMock, Mock

from motey.utils import network_utils


class TestNetworkUtils(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.expected_ip = '127.0.0.42'
        self.socketMock = Mock(Socket)
        self.socketMock.connect = MagicMock(return_value=('8.8.8.8', 53))
        self.socketMock.getsockname = MagicMock(return_value=(self.expected_ip, 12345))
        self.socketMock.close = MagicMock(return_value=None)
        self.socketMock.blub = MagicMock(return_value=None)
        network_utils.socket.socket = MagicMock(return_value=self.socketMock)

    def test_get_own_ip(self):
        resulting_ip = network_utils.get_own_ip()

        self.assertEqual(self.expected_ip, resulting_ip)
        self.assertTrue(self.socketMock.connect.called)
        self.assertTrue(self.socketMock.getsockname.called)
        self.assertTrue(self.socketMock.close.called)

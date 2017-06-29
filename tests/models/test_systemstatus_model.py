import unittest

from motey.models.systemstatus import SystemStatus


class TestSystemStatus(unittest.TestCase):
    def test_system_status_construction(self):
        resulting_system_status = SystemStatus()
        self.assertTrue(resulting_system_status.used_cpu == 0 and
                        resulting_system_status.used_memory == 0 and
                        resulting_system_status.network_tx_bytes == 0 and
                        resulting_system_status.network_rx_bytes == 0)

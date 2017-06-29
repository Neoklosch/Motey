import unittest

from motey.models.valinstancestatus import VALInstanceStatus


class TestVALInstanceStatus(unittest.TestCase):
    def test_val_instance_status_construction(self):
        resulting_val_instance_status = VALInstanceStatus()
        self.assertTrue(resulting_val_instance_status.name == None and
                        resulting_val_instance_status.image_name == None and
                        resulting_val_instance_status.created_at == None and
                        resulting_val_instance_status.status == None and
                        resulting_val_instance_status.ip == '0.0.0.0' and
                        resulting_val_instance_status.used_cpu == 0 and
                        resulting_val_instance_status.used_memory == 0 and
                        resulting_val_instance_status.network_tx_bytes == 0 and
                        resulting_val_instance_status.network_rx_bytes == 0)

class Status(object):
    def __init__(self):
        self.name = None
        self.image_name = None
        self.created_at = None
        self.status = None
        self.ip = '0.0.0.0'
        self.used_memory = 0
        self.used_cpu = 0
        self.network_tx_bytes = 0
        self.network_rx_bytes = 0

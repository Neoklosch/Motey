class SystemStatus(object):
    def __init__(self):
        self.used_memory = 0
        self.used_cpu = 0
        self.network_tx_bytes = 0
        self.network_rx_bytes = 0
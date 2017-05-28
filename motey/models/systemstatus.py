class SystemStatus(object):
    """
    Model which represents the status of the whole system.
    Possible status values are:
     * used_memory
     * used_cpu
     * network_tx_bytes
     * network_rx_bytes
    """

    def __init__(self):
        """
        Constructor of the model.
        Possible status values are:
         * used_memory
         * used_cpu
         * network_tx_bytes
         * network_rx_bytes
        """
        self.used_memory = 0
        self.used_cpu = 0
        self.network_tx_bytes = 0
        self.network_rx_bytes = 0

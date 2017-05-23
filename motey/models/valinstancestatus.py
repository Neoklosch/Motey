class VALInstanceStatus(object):
    """
    Model which represents the status of an VAL instance.
    Possible status values are:
        * name
        * image_name
        * created_at
        * status
        * ip
        * used_memory
        * used_cpu
        * network_tx_bytes
        * network_rx_bytes
    """
    def __init__(self):
        """
        Constructor of the class.
        Possible status values are:
            * name
            * image_name
            * created_at
            * status
            * ip
            * used_memory
            * used_cpu
            * network_tx_bytes
            * network_rx_bytes
        """
        self.name = None
        self.image_name = None
        self.created_at = None
        self.status = None
        self.ip = '0.0.0.0'
        self.used_memory = 0
        self.used_cpu = 0
        self.network_tx_bytes = 0
        self.network_rx_bytes = 0

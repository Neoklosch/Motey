class ServiceState(object):
    """
    Enum with service states.
     * INITIAL
     * INSTANTIATING
     * RUNNING
     * STOPPING
     * TERMINATED
     * ERROR
    """
    INITIAL = 0
    INSTANTIATING = 1
    RUNNING = 2
    STOPPING = 3
    TERMINATED = 4
    ERROR = 5

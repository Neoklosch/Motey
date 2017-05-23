import uuid


class Service(object):
    def __init__(self):
        self.id = uuid.uuid4().hex
        self.name = ''
        self.state = None
        self.images = []

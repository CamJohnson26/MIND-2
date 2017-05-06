import uuid


class GuidMapper:

    guid_map = {}

    def __init__(self):
        self.guid_map = {}

    def get(self, key):
        try:
            return self.guid_map[key]
        except KeyError:
            self.guid_map[key] = uuid.uuid4()
            return self.guid_map[key]

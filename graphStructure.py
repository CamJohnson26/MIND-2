import uuid
import json


class GraphStructure:

    nodes = []
    name = ""
    guid = ""

    def __init__(self, nodes, name):
        self.nodes = nodes
        self.name = name
        self.guid = uuid.uuid4()

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "GraphStructure"}
        rv["name"] = self.name
        rv["guid"] = str(self.guid)
        rv["nodes"] = [a.get_json() for a in self.nodes if a is not None]
        return rv

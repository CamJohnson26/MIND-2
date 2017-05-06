import json
from os import urandom

class ChainGraph:
    """
    A linear list of graph nodes which can have multiple branches
    """

    def __init__(self, nodes, name):
        self.nodes = nodes
        self.name = name
        self.guid = urandom(16)

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def __repr__(self):
        return json.dumps(self.get_json())

    def get_json(self):
        """
        Get JSON representation of class

        :return: str
        """
        rv = {"class": "ChainGraph"}
        rv["name"] = self.name
        rv["guid"] = str(self.guid)
        rv["nodes"] = [a.get_json() for a in self.nodes if a is not None]
        return rv
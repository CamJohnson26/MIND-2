from os import urandom
import json


class GraphStructure:
    """
    Framework for flowGraph and chainGraph
    """
    nodes = []
    name = ""
    guid = ""

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
        rv = {"class": "GraphStructure"}
        rv["name"] = self.name
        rv["guid"] = str(self.guid)
        rv["nodes"] = [a.get_json() for a in self.nodes if a is not None]
        return rv

import json


class ChainGraph:
    """
    A linear list of graph nodes which can have multiple branches
    """

    graph = None

    def __init__(self, graph):
        self.graph = graph

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
        rv["graph"] = self.graph.get_json()
        return rv

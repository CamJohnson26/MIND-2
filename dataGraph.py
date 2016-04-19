import json


class DataGraph:

    graph = None

    def __init__(self, graph):
        self.graph = graph

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "DataGraph"}
        rv["graph"] = self.graph.get_json()
        return rv

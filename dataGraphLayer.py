import json
from graphStructure import GraphStructure
from dataGraph import DataGraph
from dataGraphFlattener import DataGraphFlattener


class DataGraphLayer:

    dataGraph = None
    bridgeNodes = []
    dataGraphFlattener = None
    parentLayer = None

    def __init__(self, parentLayer):
        self.parentLayer = parentLayer
        graph = GraphStructure([], "DataLayer")
        self.dataGraph = DataGraph(graph)
        self.bridgeNodes = []
        self.dataGraphFlattener = DataGraphFlattener(self.dataGraph)

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "DataGraph"}
        rv["dataGraph"] = self.dataGraph.get_json()
        rv["bridgeNodes"] = [a.get_json() for a in self.bridgeNodes]
        return rv

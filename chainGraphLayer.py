import json
from graphStructure import GraphStructure
from chainGraph import ChainGraph
from chainGraphFlattener import ChainGraphFlattener


class ChainGraphLayer:

    chainGraph = None
    bridgeNodes = []
    chainGraphFlattener = None
    parentLayer = None

    def __init__(self, parentLayer):
        self.parentLayer = parentLayer
        graph = GraphStructure([], "DataLayer")
        self.chainGraph = ChainGraph(graph)
        self.bridgeNodes = []
        self.chainGraphFlattener = ChainGraphFlattener(self.chainGraph)

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def classify(self, dataClasses):
        for node in self.chainGraph.graph.nodes:
            node.classify(dataClasses)

    def get_json(self):
        rv = {"class": "ChainGraph"}
        rv["chainGraph"] = self.chainGraph.get_json()
        rv["bridgeNodes"] = [a.get_json() for a in self.bridgeNodes]
        return rv

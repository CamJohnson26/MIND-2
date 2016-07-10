import json
from graphNode import GraphNode
from chainGraph import ChainGraph
from graphStructure import GraphStructure


class DataClass:

    flowGraph = None
    dataClassIndex = 0
    dataClassString = ""

    def __init__(self, flowGraph, dataClassIndex, dataClassString):
        self.flowGraph = flowGraph
        self.dataClassIndex = dataClassIndex
        self.dataClassString = dataClassString

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "DataClass"}
        rv["flowGraph"] = self.flowGraph.get_json()
        rv["dataClassIndex"] = self.dataClassIndex
        rv["dataClassString"] = self.dataClassString
        return rv

    def matches(self, dataNode):
        if type(dataNode.parsedData) in [str, unicode]:
            nodes = [GraphNode(dataNode)]
            graphStructure = GraphStructure(nodes, self.dataClassString)
            chainGraph = ChainGraph(graphStructure)
        else:
            chainGraph = dataNode.parsedData
        return self.flowGraph.matches_chainGraph(chainGraph)

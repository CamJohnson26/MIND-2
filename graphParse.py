from graphNode import GraphNode
from graphStructure import GraphStructure
from chainGraph import ChainGraph
import json


class GraphParse:
    """
    Deprecated? Convert this class to graph stepper?
    """
    name = ""
    dataGraph = None
    current = None

    def __init__(self, name):
        self.name = name
        self.dataGraph = None
        self.current = None

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def __repr__(self):
        return json.dumps(self.get_json())

    def get_json(self):
        """
        Get JSON representation of class

        :return: str
        """
        rv = {"class": "GraphParse"}
        rv["chainGraph"] = self.chainGraph.get_json()
        rv["name"] = str(self.name)
        rv["current"] = get_json()
        return rv

    def addObject(self, dataPoint):
        """
        Who knows..

        :param dataPoint:
        :return:
        """
        graphNode = GraphNode(dataPoint)
        if not self.chainGraph:
            graph = GraphStructure([graphNode], self.name)
            self.chainGraph = ChainGraph(graph)
            self.current = graphNode
        else:
            self.chainGraph.graph.nodes.append(graphNode)
            self.current.nexts.append(graphNode)
            self.current = graphNode

import json
from graphStructure import GraphStructure
from chainGraph import ChainGraph
from chainGraphFlattener import ChainGraphFlattener
from bridgeNode import BridgeNode
from Utilities.graphNodeConstructor import graph_node_from_cursor


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

    def save_cursor(self, graphNode, cursor):
        newNode = graph_node_from_cursor(cursor)
        self.chainGraph.graph.nodes.append(newNode)
        bridge = BridgeNode(cursor.anchorPoint, graphNode, newNode)
        self.bridgeNodes.append(bridge)
        self.set_node_nexts(newNode, cursor)

    def set_node_nexts(self, graphNode, cursor):
        for node in cursor.graphCursor.previousNodes:
            for bridgeNode in self.bridgeNodes:
                if bridgeNode.endGraphNode.guid == node.guid:
                    if bridgeNode.targetGraphNode.guid != graphNode.guid:
                        bridgeNode.targetGraphNode.nexts.append(graphNode)

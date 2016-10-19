import json
from graphStructure import GraphStructure
from chainGraph import ChainGraph
from chainGraphFlattener import ChainGraphFlattener
from bridgeNode import BridgeNode
from Utilities.graphNodeConstructor import graph_nodes_from_cursor
from Utilities.dataClassFileManager import DataClassFileManager


class ChainGraphLayer:
    """
    Container for chainGraphs and their associated bridgeNodes
    """
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

    def __repr__(self):
        return json.dumps(self.get_json())

    def get_json(self):
        """
        Get JSON representation of class

        :return: str
        """
        rv = {"class": "ChainGraph"}
        rv["chainGraph"] = self.chainGraph.get_json()
        rv["bridgeNodes"] = [a.get_json() for a in self.bridgeNodes]
        return rv

    def classify(self, dataTypes):
        """
        Given a list of dataTypes, apply a class to each node in the chainGraph

        :param dataTypes:
        :return: None
        """
        dataClasses = {}
        for dataType in dataTypes:
            dataClassName = dataType.dataClasses["dataIndex"]
            dataTypeName = dataType.dataTypeName
            dcfm = DataClassFileManager()
            dataClasses[dataTypeName] = dcfm.loadObjects(dataClassName)
        for node in self.chainGraph.graph.nodes:
            if node.dataClasses["dataIndex"] is None:
                matches = node.get_matching_classes(dataClasses)
                try:
                    c = matches.pop()
                    node.rollup_dataClass(c)
                    node.dataClasses["dataIndex"] = c
                except IndexError:
                    pass
                for c in matches:
                    copy = self.copy_node(node)
                    copy.rollup_dataClass(c)
                    copy.dataClasses["dataIndex"] = c

    def copy_node(self, node):
        """
        Given a graphNode from the chainGraph, create a duplicate in the chainGraph

        :param node: graphNode
        :return: graphNode
        """
        copy = node.get_copy()
        for n in self.chainGraph.graph.nodes:
            if node in n.nexts:
                n.nexts.append(copy)
        bncopies = []
        for bn in self.bridgeNodes:
            if bn.targetGraphNode.guid == node.guid:
                bncopy = bn.get_copy()
                bncopy.targetGraphNode = copy
                bncopies.append(bncopy)
        index = self.chainGraph.graph.nodes.index(node) + 1
        self.chainGraph.graph.nodes.insert(index, copy)
        self.bridgeNodes.extend(bncopies)
        return copy

    def save_cursor(self, graphNode, cursor):
        """
        Given a cursor and a start node, create bridgeNodes for this chainGraphLayer

        :param graphNode: start nodde in the chain graph
        :param cursor: some graphCursor with end node and target node information
        :return: None
        """
        newNodes = graph_nodes_from_cursor(cursor)
        for newNode in newNodes:
            self.chainGraph.graph.nodes.append(newNode)
            bridge = BridgeNode(cursor.anchorPoint, graphNode, newNode)
            self.bridgeNodes.append(bridge)
            self.set_node_nexts(newNode, cursor)

    def set_node_nexts(self, graphNode, cursor):
        """
        Given a graphNode and a cursor, scan the bridgeNodes for something. Ugh bad code.

        :param graphNode:
        :param cursor:
        :return:
        """
        for node in cursor.graphCursor.previousNodes:
            for bridgeNode in self.bridgeNodes:
                if bridgeNode.endGraphNode.guid == node.guid:
                    if bridgeNode.targetGraphNode.guid != graphNode.guid:
                        bridgeNode.targetGraphNode.nexts.append(graphNode)

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

    def copy_node(self, graphNode):
        """
        Given a graphNode from the chainGraph, create a duplicate in the chainGraph

        :param graphNode: graphNode
        :return: graphNode
        """
        copy = graphNode.get_copy()
        for n in self.chainGraph.graph.nodes:
            if graphNode in n.nexts:
                n.nexts.append(copy)
        bncopies = []
        for bn in self.bridgeNodes:
            if bn.targetGraphNode.guid == graphNode.guid:
                bncopy = bn.get_copy()
                bncopy.targetGraphNode = copy
                bncopies.append(bncopy)
        index = self.chainGraph.graph.nodes.index(graphNode) + 1
        self.chainGraph.graph.nodes.insert(index, copy)
        self.bridgeNodes.extend(bncopies)
        return copy

    def apply_cursor_to_chain_graph_layer(self, graph_node, cursor):
        """
        Given a cursor and an end node, create bridgeNodes for this chainGraphLayer

        :param graphNode: endNode in the chain graph
        :param cursor: some graphCursor with end node and target node information
        :return: None
        """
        new_chain_graph_nodes = [a for a in self.chainGraph.graph.nodes]
        new_bridge_nodes = [a for a in self.bridgeNodes]
        newNodes = graph_nodes_from_cursor(cursor)
        for newNode in newNodes:
            new_chain_graph_nodes.append(newNode)
            bridge = BridgeNode(cursor.anchorPoint, graph_node, newNode)
            new_bridge_nodes.append(bridge)
            for target in self.get_previous_targets(newNode, new_bridge_nodes, cursor.graphCursor.previousNodes):
                target.nexts.append(newNode)
        return new_bridge_nodes, new_chain_graph_nodes

    def get_previous_targets(self, graph_node, bridge_nodes, previous_nodes):
        """
        Given a target graph_node, a list of bridge_nodes, and a cursor find all the previous node for that graph_node

        :param graphNode:
        :param cursor:
        :return:
        """
        previous_targets = []
        # Loop through the nodes that came before this cursor
        for prev_node in previous_nodes:
            for bridge_node in bridge_nodes:
                # Find the bridge node that came before this cursor
                if bridge_node.endGraphNode.guid == prev_node.guid:
                    # Make sure this graph node isn't the bridge node's target
                    if bridge_node.targetGraphNode.guid != graph_node.guid:
                        # return this bridge_node's target
                        previous_targets.append(bridge_node.targetGraphNode)
        return previous_targets

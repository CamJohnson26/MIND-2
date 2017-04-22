import json
from MIND2.chainGraph import ChainGraph
from MIND2.bridgeNode import BridgeNode
from MIND2.Utilities.constructors import graph_nodes_from_cursor
from MIND2.Utilities.fileManager import FileManager


class ChainGraphLayer:
    """
    Container for chainGraphs and their associated bridgeNodes
    """
    chainGraph = None
    bridgeNodes = []
    parentLayer = None

    def __init__(self, parentLayer):
        self.parentLayer = parentLayer
        self.chainGraph = ChainGraph([], "DataLayer")
        self.bridgeNodes = []

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

    def classify_new(self, dataTypes):
        """
        Given a list of dataTypes, apply a class to each node in the chainGraph

        :param dataTypes:
        :return: None
        """
        dataClasses = {}
        for dataType in dataTypes:
            dataClasses[dataType.dataTypeName] = dataType.dataClasses["dataIndex"]
        for node in self.chainGraph.nodes:
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
            file_manager = FileManager()
            dataClasses[dataTypeName] = file_manager.load_data_classes_old(dataClassName)
        for node in self.chainGraph.nodes:
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

    def apply_cursor_to_chain_graph_layer(self, cursor):
        """
        Given a cursor and an end node, create bridgeNodes for this chainGraphLayer

        :param graphNode: endNode in the chain graph
        :param cursor: some graphCursor with end node and target node information
        :return: None
        """
        new_chain_graph_nodes = []
        new_bridge_nodes = []
        newNodes = graph_nodes_from_cursor(cursor)
        for newNode in newNodes:
            new_chain_graph_nodes.append(newNode)
            bridge = BridgeNode(cursor.start_node, cursor.end_node, newNode)
            new_bridge_nodes.append(bridge)
            for target in self.get_previous_targets(newNode, new_bridge_nodes, cursor.previousNodes):
                target.nexts.append(newNode)
        return new_bridge_nodes, new_chain_graph_nodes

    # Next step, get this out of chaingraphlayer
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

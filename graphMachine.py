from dataNode import DataNode
from graphNode import GraphNode
from bridgeNode import BridgeNode
from graphStructure import GraphStructure
from chainGraph import ChainGraph
from flowGraphCursor import FlowGraphCursor
from chainGraphLayer import ChainGraphLayer
from dataType import DataType
import json


class GraphMachine:
    cursors = []
    flowGraphs = []
    chainGraphLayer = None
    openNodes = []

    def __init__(self, flowGraphs, parentChainGraphLayer):
        self.cursors = []
        self.flowGraphs = flowGraphs
        self.chainGraphLayer = ChainGraphLayer(parentChainGraphLayer)
        self.openNodes = []

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "FlowGraphCursor"}
        rv["flowGraph"] = self.flowGraph.get_json()
        return rv

    def feed(self, graphNode):
        for flowGraph in self.flowGraphs:
            flowGraphCursor = FlowGraphCursor(flowGraph, graphNode)
            self.cursors.append(flowGraphCursor)
        self.clean_open_nodes(graphNode)
        new_cursors = []
        for cursor in self.cursors:
            if cursor.graphCursor.feed(graphNode):
                if cursor.graphCursor.cursor_complete():
                    newNode = self.create_graph_node(cursor)
                    self.chainGraphLayer.chainGraph.graph.nodes.append(newNode)
                    bridge = BridgeNode(cursor.anchorPoint, graphNode, newNode)
                    self.chainGraphLayer.bridgeNodes.append(bridge)
                    self.set_node_nexts_from_open_nodes(newNode)
                    self.openNodes.append(graphNode)
                else:
                    new_cursors.append(cursor)
        self.cursors = new_cursors

    def create_graph_node(self, cursor):
        dataTypeName = cursor.graphCursor.graph.graph.name
        parsedGraph = GraphStructure(cursor.graphCursor.parsedData, dataTypeName)
        parsedData = ChainGraph(parsedGraph)

        def matchFunction(test):
            if not len(test) == len(self.parsedData):
                return False
            for i in range(0, len(test)):
                if not test[i].matches(self.parsedData[i]):
                    return False
            return True

        dataType = DataType(dataTypeName, matchFunction)
        dataNode = DataNode(dataType, parsedData)
        graphNode = GraphNode(dataNode)
        return graphNode

    def clean_open_nodes(self, graphNode):
        new_open_nodes = []
        for n in self.openNodes:
            node_open = False
            for c in self.cursors:
                if n.guid == c.anchorPoint.guid:
                    node_open = True
                for i in n.nexts:
                    if i.guid == c.anchorPoint.guid:
                        node_open = True
            if node_open:
                new_open_nodes.append(n)
        self.openNodes = new_open_nodes

    def set_node_nexts_from_open_nodes(self, graphNode):
        for openNode in self.openNodes:
            for bridgeNode in self.chainGraphLayer.bridgeNodes:
                if bridgeNode.endGraphNode.guid == openNode.guid:
                    bridgeNode.targetGraphNode.nexts.append(graphNode)

    def feed_chain_graph_layer(self, chainGraphLayer):
        for d in chainGraphLayer.chainGraph.graph.nodes:
            self.feed(d)

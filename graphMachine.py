from bridgeNode import BridgeNode
from flowGraphCursor import FlowGraphCursor
from chainGraphLayer import ChainGraphLayer
from Utilities.graphNodeConstructor import graph_node_from_cursor
import json


class GraphMachine:
    cursors = []
    flowGraphs = []
    chainGraphLayer = None
    memory = []

    def __init__(self, flowGraphs, parentChainGraphLayer):
        self.cursors = []
        self.flowGraphs = flowGraphs
        self.chainGraphLayer = ChainGraphLayer(parentChainGraphLayer)
        self.memory = []

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "FlowGraphCursor"}
        rv["flowGraph"] = self.flowGraph.get_json()
        return rv

    def feed(self, graphNode):
        self.update_memory(graphNode)
        self.refresh_cursors(graphNode)
        self.feed_all_cursors(graphNode)

    def refresh_cursors(self, graphNode):
        for flowGraph in self.flowGraphs:
            flowGraphCursor = FlowGraphCursor(flowGraph, graphNode)
            flowGraphCursor.graphCursor.previousNodes = [n for n in self.memory]
            self.cursors.append(flowGraphCursor)

    def update_memory(self, graphNode):
        self.memory.append(graphNode)
        if len(self.memory) > 2:
            self.memory.remove(self.memory[0])

    def feed_all_cursors(self, graphNode):
        new_cursors = []
        for cursor in self.cursors:
            if cursor.graphCursor.feed(graphNode):
                if cursor.graphCursor.cursor_complete():
                    self.save_cursor(graphNode, cursor)
                else:
                    new_cursors.append(cursor)
        self.cursors = new_cursors

    def save_cursor(self, graphNode, cursor):
        newNode = graph_node_from_cursor(cursor)
        self.chainGraphLayer.chainGraph.graph.nodes.append(newNode)
        bridge = BridgeNode(cursor.anchorPoint, graphNode, newNode)
        self.chainGraphLayer.bridgeNodes.append(bridge)
        self.set_node_nexts(newNode, cursor)

    def set_node_nexts(self, graphNode, cursor):
        for node in cursor.graphCursor.previousNodes:
            for bridgeNode in self.chainGraphLayer.bridgeNodes:
                if bridgeNode.endGraphNode.guid == node.guid:
                    if bridgeNode.targetGraphNode.guid != graphNode.guid:
                        bridgeNode.targetGraphNode.nexts.append(graphNode)

    def feed_chain_graph_layer(self, chainGraphLayer):
        for d in chainGraphLayer.chainGraph.graph.nodes:
            self.feed(d)

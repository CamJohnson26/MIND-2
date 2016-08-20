from flowGraphCursor import FlowGraphCursor
from chainGraphLayer import ChainGraphLayer
import json
import copy


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
            previousNodes = [n for n in self.memory]
            flowGraphCursor.graphCursor.previousNodes = previousNodes
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
                    self.chainGraphLayer.save_cursor(graphNode, cursor)
                new_cursors.append(cursor)
        self.cursors = new_cursors

    def feed_chain_graph_layer(self, chainGraphLayer):
        self.chainGraphLayer = ChainGraphLayer(chainGraphLayer)
        for d in chainGraphLayer.chainGraph.graph.nodes:
            self.feed(d)

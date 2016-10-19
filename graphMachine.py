from flowGraphCursor import FlowGraphCursor
from chainGraphLayer import ChainGraphLayer
import json
import copy


class GraphMachine:
    """
    Convert a chainGraphLayer to a chainGraphLayer matched to given flowGraphs
    """
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

    def __repr__(self):
        return json.dumps(self.get_json())

    def get_json(self):
        """
        Get JSON representation of class

        :return: str
        """
        rv = {"class": "FlowGraphCursor"}
        rv["flowGraph"] = get_json()
        return rv

    def feed(self, graphNode):
        """
        Insert a graphNode into this machine

        :param graphNode:
        :return: None
        """
        self.update_memory(graphNode)
        self.refresh_cursors(graphNode)
        self.feed_all_cursors(graphNode)

    def refresh_cursors(self, graphNode):
        """
        Create a new flowGraphCursor for each flowGraph

        :param graphNode:
        :return:
        """
        for flowGraph in self.flowGraphs:
            flowGraphCursor = FlowGraphCursor(flowGraph, graphNode)
            previousNodes = [n for n in self.memory]
            flowGraphCursor.graphCursor.previousNodes = previousNodes
            self.cursors.append(flowGraphCursor)

    def update_memory(self, graphNode):
        """
        Does something special for context, refactor?

        :param graphNode:
        :return: None
        """
        self.memory.append(graphNode)
        if len(self.memory) > 2:
            self.memory.remove(self.memory[0])

    def feed_all_cursors(self, graphNode):
        """
        Feed a graphNode into all the machine's current cursors

        :param graphNode:
        :return: None
        """
        new_cursors = []
        for cursor in self.cursors:
            if cursor.graphCursor.feed(graphNode):
                if cursor.graphCursor.cursor_complete():
                    self.chainGraphLayer.save_cursor(graphNode, cursor)
                new_cursors.append(cursor)
        self.cursors = new_cursors

    def feed_chain_graph_layer(self, chainGraphLayer):
        """
        Match a chainGraphLayer to this machine

        :param chainGraphLayer:
        :return: None
        """
        self.chainGraphLayer = ChainGraphLayer(chainGraphLayer)
        for d in chainGraphLayer.chainGraph.graph.nodes:
            self.feed(d)

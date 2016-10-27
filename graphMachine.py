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

    def feed(self, graphNode, memory, flow_graphs, cursors, chain_graph_layer):
        """
        Insert a graphNode into this machine

        :param graphNode:
        :return: None
        """
        new_cursors = [c for c in cursors]
        new_cursors.extend(self.build_flowgraphcursors(flow_graphs, graphNode, memory))
        new_cursors, bn, cgn = self.feed_all_cursors(graphNode, new_cursors, chain_graph_layer)
        return new_cursors, bn, cgn

    def build_flowgraphcursors(self, flowGraphs, anchorNode, memory):
        """
        Create a new flowGraphCursor for each flowGraph

        :param memory:
        :param flowGraphs:
        :param anchorNode:
        :return: list: List of flowGraphcursors
        """
        flowGraphCursors = []
        for flowGraph in flowGraphs:
            flowGraphCursor = FlowGraphCursor(flowGraph, anchorNode)
            previousNodes = [n for n in memory]
            flowGraphCursor.graphCursor.previousNodes = previousNodes
            flowGraphCursors.append(flowGraphCursor)
        return flowGraphCursors


    def add_graphnode_to_memory(self, graphNode, memory):
        """
        Add a graphNode to the given memory array

        :param memory: Array of nodes
        :param graphNode:
        :return: New memory array with the graphNode added
        """
        new_memory = [a for a in memory]
        new_memory.append(graphNode)
        if len(new_memory) > 2:
            new_memory.remove(new_memory[0])
        return new_memory

    def feed_all_cursors(self, graphNode, cursors, chain_graph_layer):
        """
        Feed a graphNode into all the machine's current cursors

        :param graphNode:
        :return: None
        """
        new_cursors = []
        bridge_nodes = []
        chain_graph_nodes = []
        for cursor in cursors:
            cn, ed = cursor.graphCursor.step_forward(graphNode, cursor.graphCursor.currentNodes)
            cursor.graphCursor.currentNodes, cursor.graphCursor.extracted_data = cn, ed
            if len(cn.keys()) > 0 or len(ed) > 0:
                if cursor.graphCursor.cursor_complete():
                    bn, cgn = chain_graph_layer.apply_cursor_to_chain_graph_layer(graphNode, cursor)
                    bridge_nodes.extend(bn)
                    chain_graph_nodes.extend(cgn)
                new_cursors.append(cursor)
        return new_cursors, bridge_nodes, chain_graph_nodes

    def feed_chain_graph_layer(self, chainGraphLayer):
        """
        Match a chainGraphLayer to this machine

        :param chainGraphLayer:
        :return: None
        """
        self.chainGraphLayer = ChainGraphLayer(chainGraphLayer)
        for d in chainGraphLayer.chainGraph.graph.nodes:
            self.memory = self.add_graphnode_to_memory(d, self.memory)
            self.cursors, bn, cgn = self.feed(d, self.memory, self.flowGraphs, self.cursors, self.chainGraphLayer)
            self.chainGraphLayer.bridgeNodes.extend(bn)
            self.chainGraphLayer.chainGraph.graph.nodes.extend(cgn)

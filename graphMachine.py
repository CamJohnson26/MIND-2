from flowGraphCursor import FlowGraphCursor
from chainGraphLayer import ChainGraphLayer
import json
import copy


class GraphMachine:
    """
    Convert a chainGraphLayer to a chainGraphLayer matched to given flowGraphs
    """
    cursors = []
    chainGraphLayer = None
    memory = []

    def __init__(self, parentChainGraphLayer):
        self.cursors = []
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
        rv = {"class": "GraphMachine"}
        return rv

    def feed(self, graphNode, chain_graph_layer, flow_graphs, cursors, memory):
        """
        Insert a graphNode into this machine

        :param graphNode:
        :return: None
        """
        new_cursors = [c for c in cursors]
        new_cursors.extend(self.build_flowgraphcursors(graphNode, flow_graphs, memory))
        new_cursors, bn, cgn = self.feed_all_cursors(graphNode, chain_graph_layer, new_cursors)
        return new_cursors, bn, cgn

    def build_flowgraphcursors(self, anchorNode, flowGraphs, memory):
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

    def feed_all_cursors(self, graphNode, chain_graph_layer, cursors):
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

    def feed_chain_graph_layer(self, chainGraphLayer, flow_graphs):
        """
        Match a chainGraphLayer to this machine

        :param chainGraphLayer:
        :return: None
        """
        memory = []
        cursors = []
        new_chain_graph_layer = ChainGraphLayer(chainGraphLayer)
        for n in chainGraphLayer.chainGraph.graph.nodes:
            memory = self.add_graphnode_to_memory(n, memory)
            cursors, bn, cgn = self.feed(n, chainGraphLayer, flow_graphs, cursors, memory)
            new_chain_graph_layer.bridgeNodes.extend(bn)
            new_chain_graph_layer.chainGraph.graph.nodes.extend(cgn)
        return new_chain_graph_layer

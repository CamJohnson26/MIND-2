from graphCursor import GraphCursor
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
            flowGraphCursor = GraphCursor(flowGraph, flowGraph.startNodes, anchorNode)
            previousNodes = [n for n in memory]
            flowGraphCursor.previousNodes = previousNodes
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
            new_cursor = cursor.get_copy()
            cn, ed, sn, en = new_cursor.step_forward(graphNode, new_cursor.currentNodes, new_cursor.start_node, new_cursor.end_node)
            new_cursor.currentNodes, new_cursor.extracted_data = cn, ed
            new_cursor.start_node, new_cursor.end_node = sn, en
            if len(cn.keys()) > 0 or len(ed) > 0:
                if new_cursor.cursor_complete():
                    bn, cgn = chain_graph_layer.apply_cursor_to_chain_graph_layer(new_cursor)
                    bridge_nodes.extend(bn)
                    chain_graph_nodes.extend(cgn)
                new_cursors.append(new_cursor)
        return new_cursors, bridge_nodes, chain_graph_nodes

    def feed_chain_graph_layer(self, chainGraphLayer, flow_graphs):
        """
        Match a chainGraphLayer to this machine

        :param chainGraphLayer:
        :return: None
        """
        return self.multi_layer_feed([chainGraphLayer.chainGraph.nodes[0]], chainGraphLayer, flow_graphs)

    def unknown(self, graph_node, flow_graphs, memory, chainGraphLayer):
        memory = self.add_graphnode_to_memory(graph_node, memory)
        new_cursors = self.build_flowgraphcursors(graph_node, flow_graphs, memory)
        bridge_nodes = []
        chain_graph_nodes = []
        stack = [([graph_node], new_cursors)]
        while len(stack) > 0:
            next_process = stack.pop()
            nodes = [a for a in next_process[0] if a is not None]
            cursors = next_process[1]
            for node in nodes:
                temp, bn, cgn = self.feed_all_cursors(node, chainGraphLayer, cursors)
                bridge_nodes.extend(bn)
                chain_graph_nodes.extend(cgn)
                if len(temp) > 0:
                    stack.append((node.nexts, temp))
        return bridge_nodes, chain_graph_nodes, memory

    def multi_layer_feed(self, current_nodes, chainGraphLayer, flow_graphs):
        new_chain_graph_layer = ChainGraphLayer(chainGraphLayer)
        dynamic_memory = {}
        memory_map = {}
        memory = []
        while 0 < len(current_nodes):
            new_current_nodes = []
            for node in current_nodes:
                memory_map[node.guid] = [a for a in memory]
                if not node.guid in dynamic_memory:
                    bn, cgn, memory = self.unknown(node, flow_graphs, memory_map[node.guid], chainGraphLayer)
                    new_chain_graph_layer.bridgeNodes.extend(bn)
                    new_chain_graph_layer.chainGraph.nodes.extend(cgn)
                    dynamic_memory[node.guid] = bn
                new_current_nodes.extend([nex for nex in node.nexts if nex is not None])
            current_nodes = new_current_nodes
        return self.update_bridge_nodes(new_chain_graph_layer, dynamic_memory)

    def update_bridge_nodes(self, new_chain_graph_layer, dynamic_memory):
        for bridge_node in new_chain_graph_layer.bridgeNodes:
            current_nexts = [a for a in bridge_node.endGraphNode.nexts if a is not None]
            if bridge_node.endGraphNode.guid != bridge_node.startGraphNode.guid:
                while len([n for n in current_nexts if n.guid in dynamic_memory]) == 0 and None not in current_nexts:
                    current_nexts = sum([n.nexts for n in current_nexts], [])
            bridge_node.targetGraphNode.nexts = sum([[a.targetGraphNode for a in dynamic_memory[n.guid]] for n in current_nexts], [])
            if len(bridge_node.targetGraphNode.nexts) == 0:
                bridge_node.targetGraphNode.nexts = [None]
        return new_chain_graph_layer

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
        return self.multi_layer_feed([chainGraphLayer.chainGraph.graph.nodes[0]], chainGraphLayer, flow_graphs)
        # memory = []
        # cursors = []
        # new_chain_graph_layer = ChainGraphLayer(chainGraphLayer)
        # for n in chainGraphLayer.chainGraph.graph.nodes:
        #     memory = self.add_graphnode_to_memory(n, memory)
        #     cursors, bn, cgn = self.feed(n, chainGraphLayer, flow_graphs, cursors, memory)
        #     new_chain_graph_layer.bridgeNodes.extend(bn)
        #     new_chain_graph_layer.chainGraph.graph.nodes.extend(cgn)
        # return new_chain_graph_layer

    def multi_layer_feed(self, sn, chainGraphLayer, flow_graphs):
        dynamic_memory = {}
        new_chain_graph_layer = ChainGraphLayer(chainGraphLayer)
        memory_map = {}
        for n in sn:
            memory_map[n.guid] = []
        # Loop until the nexts array is empty
        while len(sn) > 0:
            new_sn = []
            # Loop through each next node
            for n in sn:
                bridge_nodes = []
                chain_graph_nodes = []
                if n:
                    # Break if it's already been processed
                    if dynamic_memory.has_key(n.guid):
                        pass
                    else:
                        # Setup the variables for processing this node
                        memory = self.add_graphnode_to_memory(n, memory_map[n.guid])
                        new_cursors = self.build_flowgraphcursors(n, flow_graphs, memory)
                        # Create the stack to store the state at the current node
                        stack = [([n], new_cursors)]
                        while len(stack) > 0:
                            # Process the next element in the stack
                            next_process = stack.pop()
                            nodes = [a for a in next_process[0] if a is not None]
                            cursors = next_process[1]
                            for node in nodes:
                                # Loop through all the nodes in the current stack and feed them
                                temp, bn, cgn = self.feed_all_cursors(node, chainGraphLayer, copy.deepcopy(cursors))
                                # Store the results in the chain graph
                                bridge_nodes.extend(bn)
                                chain_graph_nodes.extend(cgn)
                                if len(temp) > 0:
                                    # If there's results, add this to the stack so that we'll feed the next element too
                                    stack.append((node.nexts, temp))
                    new_chain_graph_layer.bridgeNodes.extend(bridge_nodes)
                    new_chain_graph_layer.chainGraph.graph.nodes.extend(chain_graph_nodes)
                    # Save the results of processing this node
                    dynamic_memory[n.guid] = bridge_nodes
                    # Add the nodes next nodes to process on the next loop
                    new_sn.extend(n.nexts)
                    for m in n.nexts:
                        if m:
                            # Store each of the next nodes in memory
                            memory_map[m.guid] = [a for a in memory]
            sn = new_sn
        for b in new_chain_graph_layer.bridgeNodes:
            if b.endGraphNode.guid == b.startGraphNode.guid:
                temp = []
                for n in b.endGraphNode.nexts:
                    if n:
                        temp.extend([a.targetGraphNode for a in dynamic_memory[n.guid]])
                b.targetGraphNode.nexts = temp
            else:
                nexts = [a for a in b.endGraphNode.nexts if a is not None]
                while None not in nexts and len([n.guid for n in nexts if n.guid in dynamic_memory]) == 0 and len(nexts) != 0:
                    new_nexts = []
                    for n in nexts:
                        new_nexts.extend(n.nexts)
                    nexts = new_nexts
                new_nexts = []
                for n in nexts:
                    if n and n.guid in dynamic_memory:
                        new_nexts.extend(dynamic_memory[n.guid])
                nexts = [n.targetGraphNode for n in new_nexts]
                b.targetGraphNode.nexts = nexts
            if len(b.targetGraphNode.nexts) == 0:
                b.targetGraphNode.nexts = [None]
        return new_chain_graph_layer

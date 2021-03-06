import json
from os import urandom


class GraphCursor:
    """
    Handles the state of a graph
    """
    graph = None
    currentNodes = {}           # First node in each branch {NodeId: {"node" : Node, "parsedData": [Node, Node]}}
    extracted_data = []
    previousNodes = []
    start_node = None
    end_node = None
    anchorPoint = None

    def __init__(self, graph, startNodes, anchorPoint):
        self.graph = graph
        self.currentNodes = {}
        for n in startNodes:
            self.currentNodes[urandom(16)] = {"node": n, "parsedData": []}
        self.extracted_data = []
        self.previousNodes = []
        self.anchorPoint = anchorPoint

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def __repr__(self):
        return json.dumps(self.get_json())

    def get_json(self):
        """
        Get JSON representation of class

        :return: str
        """
        rv = {"class": "GraphCursor"}
        rv["graph"] = self.graph.get_json()
        cursors = [c.get_json() for c in self.currentNodes if c is not None]
        cursors.extend([c for c in self.currentNodes if c is None])
        rv["currentNodes"] = cursors
        rv["parsedData"] = [d.get_json() for d in self.extracted_data]
        rv["anchorPoint"] = self.anchorPoint.get_json()
        return rv

    def get_copy(self):
        new_cursor = GraphCursor(self.graph, [], self.anchorPoint)
        new_cursor.extracted_data = [a for a in self.extracted_data]
        new_cursor.previousNodes = [a for a in self.previousNodes]
        new_cursor.start_node = self.start_node
        new_cursor.end_node = self.end_node
        for key in self.currentNodes.keys():
            new_cursor.currentNodes[key] = self.currentNodes[key]
        return new_cursor

    def step_forward(self, graphNode, currentNodes, start_node, end_node):
        """
        Send the graphNode through the cursor and return the resulting cursor

        :param graphNode: The node to check for matches
        :param currentNodes: The initial state of the cursor
        :return: {NodeId: {"node" : Node, "parsedData": [Node, Node]}} the resulting state and the finished data
        """
        new_current_nodes = {}
        extracted_data = []
        for key in currentNodes.keys():
            current_node = currentNodes[key]
            if current_node["node"] and current_node["node"].matches(graphNode):
                for n in current_node["node"].nexts:
                    next_node = {"node": n, "parsedData": [a for a in current_node["parsedData"]]}
                    if current_node["node"] not in self.graph.contextNodes:
                        next_node["parsedData"].append(graphNode)
                        if start_node is None:
                            start_node = graphNode
                        end_node = graphNode
                    if n:
                        new_current_nodes[urandom(16)] = next_node
                    if not n:
                        extracted_data.append(next_node["parsedData"])
        return new_current_nodes, extracted_data, start_node, end_node

    def cursor_complete(self):
        """
        Could the cursor be finished?

        :return: boolean
        """
        return len(self.extracted_data) > 0

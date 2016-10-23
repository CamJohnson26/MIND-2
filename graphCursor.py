import json
import uuid


class GraphCursor:
    """
    Handles the state of a graph
    """
    graph = None
    currentNodes = {}           # First node in each branch {NodeId: {"node" : Node, "parsedData": [Node, Node]}}
    parsedData = []
    previousNodes = []

    def __init__(self, graph, startNodes):
        self.graph = graph
        self.currentNodes = {}
        for n in startNodes:
            self.currentNodes[uuid.uuid4()] = {"node": n, "parsedData": []}
        self.parsedData = []
        self.previousNodes = []

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
        rv["graph"] = get_json()
        cursors = [get_json() for c in self.currentNodes if c is not None]
        cursors.extend([c for c in self.currentNodes if c is None])
        rv["currentNodes"] = cursors
        rv["parsedData"] = [d.get_json() for d in self.parsedData]
        return rv

    def feed(self, graphNode):
        """
        Insert a graphNode into the graph and handle the resulting state

        :param dataPoint: graphNode
        :return: boolean: T/F value for success of feed attempt
        """
        self.currentNodes, self.parsedData = self.step_forward(graphNode, self.currentNodes)
        return len(self.currentNodes.keys()) > 0 or len(self.parsedData) > 0

    def step_forward(self, graphNode, currentNodes):
        """
        Send the graphNode through the cursor and return the resulting cursor

        :param graphNode: The node to check for matches
        :param currentNodes: The initial state of the cursor
        :return: {NodeId: {"node" : Node, "parsedData": [Node, Node]}} the resulting state and the finished data
        """
        new_current_nodes = {}
        extracted_data = []
        for key in currentNodes.keys():
            current_node = self.currentNodes[key]
            if current_node["node"] and current_node["node"].matches(graphNode):
                for n in current_node["node"].nexts:
                    next_node = {"node": n, "parsedData": [a for a in current_node["parsedData"]]}
                    if current_node["node"] not in self.graph.contextNodes:
                        next_node["parsedData"].append(graphNode)
                    if n:
                        new_current_nodes[uuid.uuid4()] = next_node
                    if not n:
                        extracted_data.append(next_node["parsedData"])
        return new_current_nodes, extracted_data

    def cursor_complete(self):
        """
        Could the cursor be finished?

        :return: boolean
        """
        return len(self.parsedData) > 0

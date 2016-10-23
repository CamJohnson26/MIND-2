import json
from flowGraphCursor import FlowGraphCursor


class FlowGraph:
    """
    Logical structure to represent a dataType or a dataClass
    """
    graph = None
    startNodes = []
    contextNodes = []

    def __init__(self, graph, startNodes, contextNodes=[]):
        self.graph = graph
        self.startNodes = startNodes
        self.contextNodes = contextNodes

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def __repr__(self):
        return json.dumps(self.get_json())

    def get_json(self):
        """
        Get JSON representation of class

        :return: str
        """
        rv = {"class": "FlowGraph"}
        rv["graph"] = get_json()
        rv["startNodes"] = [str(a.guid) for a in self.startNodes]
        rv["contextNodes"] = [str(a.guid) for a in self.contextNodes]
        return rv

    def matches_chainGraph(self, chainGraph):
        """

        :param chainGraph:
        :return: boolean
        """
        cursor = FlowGraphCursor(self, chainGraph.graph.nodes[0])
        for graphNode in chainGraph.graph.nodes:
            cn, ed = cursor.graphCursor.step_forward(graphNode, cursor.graphCursor.currentNodes)
            cursor.graphCursor.currentNodes, cursor.graphCursor.extracted_data = cn, ed
            if not (len(cn.keys()) > 0 or len(ed) > 0):
                return False
        if cursor.graphCursor.cursor_complete():
            return True
        return False

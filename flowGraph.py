import json
from graphCursor import GraphCursor
from os import urandom

class FlowGraph:
    """
    Logical structure to represent a dataType or a dataClass
    """
    def __init__(self, nodes, name, startNodes, contextNodes=[]):
        self.startNodes = startNodes
        self.contextNodes = contextNodes
        self.nodes = nodes
        self.name = name
        self.guid = urandom(16)

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
        rv["startNodes"] = [str(a.guid) for a in self.startNodes]
        rv["contextNodes"] = [str(a.guid) for a in self.contextNodes]
        rv["name"] = self.name
        rv["guid"] = str(self.guid)
        rv["nodes"] = [a.get_json() for a in self.nodes if a is not None]
        return rv

    def matches_chainGraph(self, chainGraph):
        """

        :param chainGraph:
        :return: boolean
        """
        cursor = GraphCursor(self, self.startNodes, chainGraph.nodes[0])
        for graphNode in chainGraph.nodes:
            cn, ed, sn, en = cursor.step_forward(graphNode, cursor.currentNodes, cursor.start_node, cursor.end_node)
            cursor.currentNodes, cursor.extracted_data = cn, ed
            cursor.start_node, cursor.end_node = sn, en
            if not (len(cn.keys()) > 0 or len(ed) > 0):
                return False
        if cursor.cursor_complete():
            return True
        return False

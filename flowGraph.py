import json
from flowGraphCursor import FlowGraphCursor


class FlowGraph:

    graph = None
    startNodes = []
    contextNodes = []

    def __init__(self, graph, startNodes, contextNodes=[]):
        self.graph = graph
        self.startNodes = startNodes
        self.contextNodes = contextNodes

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "FlowGraph"}
        rv["graph"] = self.graph.get_json()
        rv["startNodes"] = [str(a.guid) for a in self.startNodes]
        rv["contextNodes"] = [str(a.guid) for a in self.contextNodes]
        return rv

    def matches_chainGraph(self, chainGraph):
        cursor = FlowGraphCursor(self, chainGraph.graph.nodes[0])
        for graphNode in chainGraph.graph.nodes:
            if not cursor.graphCursor.feed(graphNode):
                return False
        if cursor.graphCursor.cursor_complete():
            return True
        return False

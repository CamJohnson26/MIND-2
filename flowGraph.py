import json
from graphCursor import GraphCursor


class FlowGraph:

    graph = None
    startNodes = []

    def __init__(self, graph, startNodes):
        self.graph = graph
        self.startNodes = startNodes

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "FlowGraph"}
        rv["graph"] = self.graph.get_json()
        rv["startNodes"] = [str(a.guid) for a in self.startNodes]
        return rv

    # Move this to graph stepper class
    def matches_datagraph(self, dataGraph):
        cursors = [GraphCursor(self, self.graph.nodes[0])]
        for dataPoint in dataGraph:
            new_cursors = []
            for cursor in cursors:
                if cursor.matches(dataPoint):
                    for node in cursor.currendNode.nexts:
                        new_cursors.append(GraphCursor(self, node))
            cursors = new_cursors
            for cursor in new_cursors:
                if None in cursor.currentNode.nexts:
                    return True
        return False

import json


class GraphCursor:

    graph = None
    currentNodes = []
    parsedData = []

    def __init__(self, graph, startNode):
        self.graph = graph
        self.currentNodes = [startNode]
        self.parsedData = []

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "GraphCursor"}
        rv["graph"] = self.graph.get_json()
        cursors = [c.get_json() for c in self.currentNodes if c is not None]
        cursors.extend([c for c in self.currentNodes if c is None])
        rv["currentNodes"] = cursors
        rv["parsedData"] = [d.get_json() for d in self.parsedData]
        return rv

    def feed(self, dataPoint):
        new_currentNodes = []
        for c in self.currentNodes:
            if c is not None and c.matches(dataPoint):
                new_currentNodes.extend(c.nexts)
        self.parsedData.append(dataPoint)
        self.currentNodes = new_currentNodes
        return len(new_currentNodes) > 0

    def cursor_complete(self):
        return None in self.currentNodes

import json


class GraphCursor:

    graph = None
    currentNodes = []
    parsedData = []
    previousNodes = []

    def __init__(self, graph, startNodes):
        self.graph = graph
        self.currentNodes = startNodes
        self.parsedData = []
        self.previousNodes = []

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
        success = False
        new_currentNodes = []
        dataType = dataPoint.dataNode.dataType
        isContext = False
        for c in self.currentNodes:
            if c is not None and c.matches(dataPoint):
                new_currentNodes.extend(c.nexts)
                dataType = c.dataNode.dataType
                success = True
                isContext = c in self.graph.contextNodes
        dataPoint.dataNode.dataType = dataType
        if isContext is False:
            self.parsedData.append(dataPoint)
        self.currentNodes = new_currentNodes
        return success

    def cursor_complete(self):
        return None in self.currentNodes

import json
import uuid


class GraphCursor:

    graph = None
    currentNodes = {}
    parsedData = []
    previousNodes = []

    def __init__(self, graph, startNodes):
        self.graph = graph
        self.currentNodes = {}
        for n in startNodes:
            if n not in self.graph.contextNodes:
                self.currentNodes[uuid.uuid4()] = {"node": n, "parsedData":[n]}
            else:
                self.currentNodes[uuid.uuid4()] = {"node": n, "parsedData": []}
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
        self.parsedData = []
        if len([a for a in self.currentNodes if a is not None]) == 0:
            return False
        success = False
        new_currentNodes = {}
        dataType = dataPoint.dataNode.dataType
        for key in self.currentNodes.keys():
            c = self.currentNodes[key]
            if c and c["node"].matches(dataPoint):
                for n in c["node"].nexts:
                    if n:
                        temp_cursor = {}
                        temp_cursor["node"] = n
                        new_pd = [a for a in c["parsedData"]]
                        temp_cursor["parsedData"] = new_pd
                        dataType = c["node"].dataNode.dataType
                        dataPoint.dataNode.dataType = dataType
                        if c["node"] not in self.graph.contextNodes:
                            pd = temp_cursor.get("parsedData") or []
                            pd.append(dataPoint)
                            temp_cursor["parsedData"] = pd
                        new_currentNodes[uuid.uuid4()] = temp_cursor
                    else:
                        self.parsedData.append(c["parsedData"])
                success = True
        self.currentNodes = new_currentNodes
        return success

    def cursor_complete(self):
        return len(self.parsedData) > 0

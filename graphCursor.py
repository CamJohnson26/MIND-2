import json
import uuid


class GraphCursor:
    """
    Handles the state of a graph
    """
    graph = None
    currentNodes = {}
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

    def feed(self, dataPoint):
        """
        Insert a graphNode into the graph and handle the resulting state

        :param dataPoint: graphNode
        :return: boolean: T/F value for success of feed attempt
        """
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
                        dataType = c["node"].dataNode.dataType
                        dataPoint.dataNode.dataType = dataType
                        pd = [a for a in c["parsedData"]]
                        if c["node"] not in self.graph.contextNodes:
                            pd.append(dataPoint)
                        self.parsedData.append(pd)
                success = True
        self.currentNodes = new_currentNodes
        return success

    def cursor_complete(self):
        """
        Could the cursor be finished?

        :return: boolean
        """
        return len(self.parsedData) > 0

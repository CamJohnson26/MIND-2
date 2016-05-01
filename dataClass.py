import json
from flowGraphCursor import FlowGraphCursor
from graphNode import GraphNode


class DataClass:

    flowGraph = None
    dataClassIndex = 0
    dataClassString = ""

    def __init__(self, flowGraph, dataClassIndex, dataClassString):
        self.flowGraph = flowGraph
        self.dataClassIndex = dataClassIndex
        self.dataClassString = dataClassString

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "DataClass"}
        rv["flowGraph"] = self.flowGraph.get_json()
        rv["dataClassIndex"] = self.dataClassIndex
        rv["dataClassString"] = self.dataClassString
        return rv

    def matches(self, dataNode):
        graphNode = GraphNode(dataNode)
        cursor = FlowGraphCursor(self.flowGraph, graphNode)
        if cursor.graphCursor.feed(graphNode):
            if cursor.graphCursor.cursor_complete():
                return True
        return False

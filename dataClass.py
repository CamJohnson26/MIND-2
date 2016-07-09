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
        if type(dataNode.parsedData) in [str, unicode]:
            nodes = [GraphNode(dataNode)]
        else:
            nodes = dataNode.parsedData.graph.nodes
        cursor = FlowGraphCursor(self.flowGraph, nodes[0])
        for graphNode in nodes:
            if cursor.graphCursor.feed(graphNode):
                if cursor.graphCursor.cursor_complete():
                    return True
            else:
                return False
        # Create DataGraphMachine and feed data
        return False

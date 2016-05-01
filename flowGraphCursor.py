from graphCursor import GraphCursor
import json


class FlowGraphCursor:

    anchorPoint = None
    graphCursor = None

    def __init__(self, flowGraph, anchorPoint):
        self.graphCursor = GraphCursor(flowGraph, flowGraph.startNodes)
        self.anchorPoint = anchorPoint

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "FlowGraphCursor"}
        rv["graphCursor"] = self.graphCursor.get_json()
        rv["anchorPoint"] = self.anchorPoint.get_json()
        return rv

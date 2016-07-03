from graphCursor import GraphCursor
import json


class ChainGraphCursor:

    anchorPoint = None
    graphCursor = None

    def __init__(self, chainGraph, anchorPoint):
        self.graphCursor = GraphCursor(chainGraph, chainGraph.graph.nodes[0])
        self.anchorPoint = anchorPoint

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "ChainGraphCursor"}
        rv["graphCursor"] = self.graphCursor.get_json()
        rv["anchorPoint"] = self.anchorPoint.get_json()
        return rv

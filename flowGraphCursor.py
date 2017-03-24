from graphCursor import GraphCursor
import json


class FlowGraphCursor:
    """
    Handles the state of a flowGraph
    """
    anchorPoint = None
    graphCursor = None

    def __init__(self, flowGraph, anchorPoint):
        self.graphCursor = GraphCursor(flowGraph, flowGraph.startNodes)
        self.anchorPoint = anchorPoint

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def __repr__(self):
        return json.dumps(self.get_json())

    def get_json(self):
        """
        Get JSON representation of class

        :return: str
        """
        rv = {"class": "FlowGraphCursor"}
        rv["graphCursor"] = self.graphCursor.get_json()
        rv["anchorPoint"] = self.anchorPoint.get_json()
        return rv

    def get_copy(self):
        new_cursor = FlowGraphCursor(self.graphCursor.graph, [])
        new_cursor.graphCursor = self.graphCursor.get_copy()
        new_cursor.anchorPoint = self.anchorPoint
        return new_cursor

from dataNode import DataNode
from graphNode import GraphNode
from bridgeNode import BridgeNode
from graphStructure import GraphStructure
from dataGraph import DataGraph
from flowGraphCursor import FlowGraphCursor
from dataGraphLayer import DataGraphLayer
from dataType import DataType
import json


class DataGraphMachine:
    cursors = []
    flowGraphs = []
    dataGraphLayer = None

    def __init__(self, flowGraphs, parentDataGraphLayer):
        self.cursors = []
        self.flowGraphs = flowGraphs
        self.dataGraphLayer = DataGraphLayer(parentDataGraphLayer)

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "FlowGraphCursor"}
        rv["flowGraph"] = self.flowGraph.get_json()
        return rv

    def feed(self, graphNode):
        for flowGraph in self.flowGraphs:
            flowGraphCursor = FlowGraphCursor(flowGraph, graphNode)
            self.cursors.append(flowGraphCursor)
        new_cursors = []
        for cursor in self.cursors:
            if cursor.graphCursor.feed(graphNode):
                if cursor.graphCursor.cursor_complete():
                    newNode = self.create_graph_node(cursor)
                    bridge = self.create_bridge(cursor, graphNode, newNode)
                    self.dataGraphLayer.dataGraph.graph.nodes.append(newNode)
                    self.dataGraphLayer.bridgeNodes.append(bridge)
                else:
                    new_cursors.append(cursor)
        self.cursors = new_cursors

    def create_graph_node(self, cursor):
        dataTypeName = cursor.graphCursor.graph.graph.name
        parsedGraph = GraphStructure(cursor.graphCursor.parsedData, dataTypeName)
        parsedData = DataGraph(parsedGraph)

        def matchFunction(test):
            if not len(test) == len(self.parsedData):
                return False
            for i in range(0, len(test)):
                if not test[i].matches(self.parsedData[i]):
                    return False
            return True

        dataType = DataType(dataTypeName, matchFunction)
        dataNode = DataNode(dataType, parsedData)
        graphNode = GraphNode(dataNode)
        return graphNode

    def create_bridge(self, cursor, endGraphNode, targetGraphNode):
        bridgeNode = BridgeNode()
        bridgeNode.startGraphNode = cursor.anchorPoint
        bridgeNode.endGraphNode = endGraphNode
        bridgeNode.targetGraphNode = targetGraphNode
        return bridgeNode

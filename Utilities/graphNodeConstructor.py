from graphNode import GraphNode
from graphStructure import GraphStructure
from chainGraph import ChainGraph
from dataType import DataType
from dataNode import DataNode
import dataNodeConstructor
import json


def graphNodeFromJSON(inputJSON):
    inputObject = json.loads(inputJSON)
    if type(inputObject["dataNode"]) is unicode:
        dataNode = dataNodeConstructor.loadDataNode(inputObject["dataNode"])
    else:
        node_json = json.dumps(inputObject["dataNode"])
        dataNode = dataNodeConstructor.dataNodeFromJSON(node_json)
    graphNode = GraphNode(dataNode)
    graphNode.guid = inputObject["guid"]
    graphNode.nexts = []
    return graphNode


def graph_node_from_cursor(cursor):
    dataTypeName = cursor.graphCursor.graph.graph.name
    parsedGraph = GraphStructure(cursor.graphCursor.parsedData, dataTypeName)
    parsedData = ChainGraph(parsedGraph)

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

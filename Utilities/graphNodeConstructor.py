from graphNode import GraphNode
from graphStructure import GraphStructure
from chainGraph import ChainGraph
from dataType import DataType
from dataNode import DataNode
import Data.matchFunctions as matchFunctions
import dataNodeConstructor
import dataClassConstructor
import json


def graphNodeFromJSON(inputJSON):
    inputObject = json.loads(inputJSON)
    if type(inputObject["dataNode"]) is unicode:
        dataNode = dataNodeConstructor.loadDataNode(inputObject["dataNode"])
    else:
        node_json = json.dumps(inputObject["dataNode"])
        dataNode = dataNodeConstructor.dataNodeFromJSON(node_json)
    if inputObject["dataClass"] is None:
        dataClass = None
    elif type(inputObject["dataClass"]) is unicode:
        dataClass = dataClassConstructor.loadDataClass(inputObject["dataClass"])
    else:
        dataClass = dataClassConstructor.dataClassFromJSON(json.dumps(inputObject["dataClass"]))
    graphNode = GraphNode(dataNode)
    graphNode.guid = inputObject["guid"]
    graphNode.nexts = []
    graphNode.dataClass = dataClass
    return graphNode


def graph_node_from_cursor(cursor):
    dataTypeName = cursor.graphCursor.graph.graph.name
    parsedGraph = GraphStructure(cursor.graphCursor.parsedData, dataTypeName)
    parsedData = ChainGraph(parsedGraph)
    matchFunction = getattr(matchFunctions, "matchFunction")
    dataType = DataType(dataTypeName, matchFunction)
    dataNode = DataNode(dataType, parsedData)
    graphNode = GraphNode(dataNode)
    return graphNode

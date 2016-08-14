from graphNode import GraphNode
from graphStructure import GraphStructure
from chainGraph import ChainGraph
from dataType import DataType
from dataNode import DataNode
from guidMapper import GuidMapper
import Data.matchFunctions as matchFunctions
import dataNodeConstructor
import dataClassConstructor
import json


def graphNodeFromJSON(inputJSON, guidMapper=GuidMapper()):
    inputObject = json.loads(inputJSON)
    if type(inputObject["dataNode"]) is unicode:
        dataNode = dataNodeConstructor.loadDataNode(inputObject["dataNode"])
    else:
        node_json = json.dumps(inputObject["dataNode"])
        dataNode = dataNodeConstructor.dataNodeFromJSON(node_json)
    dataClasses = {}
    for key in inputObject["dataClasses"].keys():
        if not inputObject["dataClasses"][key]:
            dataClasses[key] = None
        elif type(inputObject["dataClasses"][key]) in [unicode, str]:
            dataClasses[key] = dataClassConstructor.loadDataClass(inputObject["dataClasses"][key])
        else:
            dataClasses[key] = dataClassConstructor.dataClassFromJSON(json.dumps(inputObject["dataClasses"][key]))
    graphNode = GraphNode(dataNode)
    graphNode.guid = guidMapper.get(inputObject["guid"])
    graphNode.nexts = []
    graphNode.dataClasses = dataClasses
    return graphNode


def graph_node_from_cursor(cursor):
    dataTypeName = cursor.graphCursor.graph.graph.name
    dataClasses = {"dataIndex": None}
    parsedGraph = GraphStructure(cursor.graphCursor.parsedData, dataTypeName)
    parsedData = ChainGraph(parsedGraph)
    matchFunction = getattr(matchFunctions, "matchFunction")
    dataType = DataType(dataTypeName, dataClasses, matchFunction)
    dataNode = DataNode(dataType, parsedData)
    graphNode = GraphNode(dataNode)
    return graphNode

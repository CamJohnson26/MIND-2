from graphNode import GraphNode
from graphStructure import GraphStructure
from chainGraph import ChainGraph
from dataType import DataType
from Utilities.guidMapper import GuidMapper
import Data.matchFunctions as matchFunctions
from Utilities.dataTypeFileManager import DataTypeFileManager
from Utilities.dataClassFileManager import DataClassFileManager
import json


def graphNodeFromJSON(inputJSON, guidMapper=GuidMapper()):
    inputObject = json.loads(inputJSON)
    dtfm = DataTypeFileManager()
    dcfm = DataClassFileManager()
    if type(inputObject["dataType"]) is str:
        dataType = dtfm.loadObject(inputObject["dataType"])
    else:
        node_json = json.dumps(inputObject["dataType"])
        dataType = dtfm.loadObject(node_json)
    dataClasses = {}
    for key in inputObject["dataClasses"].keys():
        if not inputObject["dataClasses"][key]:
            dataClasses[key] = None
        elif type(inputObject["dataClasses"][key]) in [str]:
            dataClasses[key] = dcfm.loadObject(inputObject["dataClasses"][key])
        else:
            dataClasses[key] = dcfm.loadObject(json.dumps(inputObject["dataClasses"][key]))
    graphNode = GraphNode(dataType)
    graphNode.guid = guidMapper.get(inputObject["guid"])
    graphNode.nexts = []
    graphNode.dataClasses = dataClasses
    return graphNode


def graph_nodes_from_cursor(cursor):
    """
    Given a flowGraph cursor, return a list of graphNodes, one for each of the parsedData pieces the cursor found

    :param cursor:
    :return:
    """
    dataTypeName = cursor.graphCursor.graph.graph.name
    dataClasses = {"dataIndex": None}
    matchFunction = getattr(matchFunctions, "matchFunction")
    dataType = DataType(dataTypeName, dataClasses, matchFunction)
    graphNodes = []
    parsedData = cursor.graphCursor.extracted_data
    for pd in parsedData:
        parsedGraph = GraphStructure(pd, dataTypeName)
        new_pd = ChainGraph(parsedGraph)
        graphNodes.append(GraphNode(dataType, new_pd))
    return graphNodes

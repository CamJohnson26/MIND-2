import json
from dataType import DataType
from chainGraph import ChainGraph
from graphNode import GraphNode
from graphStructure import GraphStructure
from Utilities.guidMapper import GuidMapper
import Data.matchFunctions as matchFunctions


def graphNodeFromJSON(inputJSON, guidMapper=GuidMapper()):
    from Utilities.dataTypeFileManager import DataTypeFileManager
    from Utilities.dataClassFileManager import DataClassFileManager
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
    dataTypeName = cursor.graph.graph.name
    dataClasses = {"dataIndex": None}
    matchFunction = getattr(matchFunctions, "matchFunction")
    dataType = DataType(dataTypeName, dataClasses, matchFunction)
    graphNodes = []
    parsedData = cursor.extracted_data
    for pd in parsedData:
        parsedGraph = GraphStructure(pd, dataTypeName)
        new_pd = ChainGraph(parsedGraph)
        graphNodes.append(GraphNode(dataType, new_pd))
    return graphNodes


def graphStructureFromJSON(inputJSON, guidMapper=GuidMapper()):
    inputObject = json.loads(inputJSON)
    name = inputObject["name"]
    nodes = []
    nodeGuids = {}
    for node in inputObject["nodes"]:
        new_node = graphNodeFromJSON(json.dumps(node), guidMapper=guidMapper)
        nodeGuids[new_node.guid] = new_node
        nodes.append(new_node)
    for node in inputObject["nodes"]:
        current_node = nodeGuids[guidMapper.get(node["guid"])]
        new_nexts = []
        for next_id in node["nexts"]:
            if next_id is None:
                new_nexts.append(None)
            else:
                new_nexts.append(nodeGuids[guidMapper.get(next_id)])
        current_node.nexts = new_nexts
    graphStructure = GraphStructure(nodes, name)
    graphStructure.guid = guidMapper.get(inputObject["guid"])
    return graphStructure


def chainGraphFromJSON(inputJSON):
    inputObject = json.loads(inputJSON)
    graph = graphStructureFromJSON(json.dumps(inputObject["graph"]))
    chainGraph = ChainGraph(graph)
    return chainGraph


def chainGraphFromString(inputString):
    from Utilities.dataTypeFileManager import DataTypeFileManager
    testDataGraphNodes = []
    previousNode = None
    dtfm = DataTypeFileManager()
    dataTypes = [dtfm.loadObject("letter.json"), dtfm.loadObject("number.json"), dtfm.loadObject("punctuation.json"), dtfm.loadObject("whiteSpace.json")]
    for c in inputString:
        cDataTypeName = "char"
        for dataType in dataTypes:
            if dataType.matches(c):
                cDataTypeName = dataType.dataTypeName
        cDataType = dtfm.loadObject(cDataTypeName + ".json")
        cGraphNode = GraphNode(cDataType, c)
        testDataGraphNodes.append(cGraphNode)
        if previousNode:
            previousNode.nexts.append(cGraphNode)
        previousNode = cGraphNode
    testDataGraphNodes[-1].nexts.append(None)
    testDataGraph = GraphStructure(testDataGraphNodes, "character_stream")
    return ChainGraph(testDataGraph)


def chainGraphLayerFromString(inputString):
    from chainGraphLayer import ChainGraphLayer
    from Utilities.dataTypeFileManager import DataTypeFileManager
    dtfm = DataTypeFileManager()
    chainGraphLayer = ChainGraphLayer(None)
    chainGraphLayer.chainGraph = chainGraphFromString(inputString)
    chainGraphLayer.classify([dtfm.loadObject("letter.json")])
    return chainGraphLayer

import json
from MIND2.dataType import DataType
from MIND2.chainGraph import ChainGraph
from MIND2.graphNode import GraphNode
from MIND2.Utilities.guidMapper import GuidMapper
import MIND2.Data.matchFunctions as matchFunctions


def graphNodeFromJSON_new(inputJSON, data_types, guidMapper=GuidMapper()):
    from MIND2.Utilities.fileManager import FileManager
    inputObject = json.loads(inputJSON)
    file_manager = FileManager()
    data_type = data_types[inputObject["dataType"]]
    dataClasses = {}
    for key in inputObject["dataClasses"].keys():
        if not inputObject["dataClasses"][key]:
            dataClasses[key] = None
        elif type(inputObject["dataClasses"][key]) is str:
            data_classes = data_type.dataClasses[key]
            data_class_name = inputObject["dataClasses"][key]
            data_class = data_classes[data_class_name]
            dataClasses[key] = data_class
            dataClasses[key] = data_type.dataClasses[key][inputObject["dataClasses"][key]]
    graphNode = GraphNode(data_type)
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
    dataTypeName = cursor.graph.name
    dataClasses = {"dataIndex": None}
    matchFunction = getattr(matchFunctions, "matchFunction")
    dataType = DataType(dataTypeName, dataClasses, matchFunction)
    graphNodes = []
    parsedData = cursor.extracted_data
    for pd in parsedData:
        new_pd = ChainGraph(pd, dataTypeName)
        graphNodes.append(GraphNode(dataType, new_pd))
    return graphNodes

def graphFromJSON(inputJSON, data_types, guidMapper=GuidMapper()):
    inputObject = json.loads(inputJSON)
    name = inputObject["name"]
    nodes = []
    nodeGuids = {}
    for node in inputObject["nodes"]:
        new_node = graphNodeFromJSON_new(json.dumps(node), data_types, guidMapper=guidMapper)
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
    return nodes, name

def chainGraphFromJSON(inputJSON):
    inputObject = json.loads(inputJSON)
    nodes, name = graphFromJSON(json.dumps(inputObject["graph"]))
    chainGraph = ChainGraph(nodes, name)
    return chainGraph


def chainGraphFromString(inputString):
    from MIND2.Utilities.fileManager import FileManager
    testDataGraphNodes = []
    previousNode = None
    file_manager = FileManager()
    # TODO: Need to update this to load the level 0 folder and pass it into one of the lower methods
    low_level_data_types = file_manager.load_level("level0","Data\\Core", {})
    dataTypes = [
        file_manager.load_data_type("letter", "Data\\Core\\level1", low_level_data_types=low_level_data_types),
        file_manager.load_data_type("number", "Data\\Core\\level1", low_level_data_types=low_level_data_types),
        file_manager.load_data_type("punctuation", "Data\\Core\\level1", low_level_data_types=low_level_data_types),
        file_manager.load_data_type("white_space", "Data\\Core\\level1", low_level_data_types=low_level_data_types)
    ]
    for c in inputString:
        cDataTypeName = "char"
        for dataType in low_level_data_types.values():
            if dataType.matches(c):
                cDataTypeName = dataType.dataTypeName
        cDataType = file_manager.load_data_type(cDataTypeName, "Data\\Core\\level1", low_level_data_types=low_level_data_types)
        cGraphNode = GraphNode(cDataType, c)
        testDataGraphNodes.append(cGraphNode)
        if previousNode:
            previousNode.nexts.append(cGraphNode)
        previousNode = cGraphNode
    testDataGraphNodes[-1].nexts.append(None)
    return ChainGraph(testDataGraphNodes, "character_stream")


def chainGraphLayerFromString(inputString):
    from MIND2.chainGraphLayer import ChainGraphLayer
    from MIND2.Utilities.fileManager import FileManager
    file_manager = FileManager()
    chainGraphLayer = ChainGraphLayer(None)
    chainGraphLayer.chainGraph = chainGraphFromString(inputString)
    return chainGraphLayer

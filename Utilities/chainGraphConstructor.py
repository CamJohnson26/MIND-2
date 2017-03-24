from chainGraph import ChainGraph
from graphNode import GraphNode
from graphStructure import GraphStructure
from chainGraphLayer import ChainGraphLayer
from Utilities.dataTypeFileManager import DataTypeFileManager
import Utilities.graphStructureConstructor
import json


def chainGraphFromJSON(inputJSON):
    inputObject = json.loads(inputJSON)
    graph = graphStructureConstructor.graphStructureFromJSON(json.dumps(inputObject["graph"]))
    chainGraph = ChainGraph(graph)
    return chainGraph


def chainGraphFromString(inputString):
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
    dtfm = DataTypeFileManager()
    chainGraphLayer = ChainGraphLayer(None)
    chainGraphLayer.chainGraph = chainGraphFromString(inputString)
    chainGraphLayer.classify([dtfm.loadObject("letter.json")])
    return chainGraphLayer

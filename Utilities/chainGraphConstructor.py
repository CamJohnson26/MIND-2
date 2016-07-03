from chainGraph import ChainGraph
from dataType import DataType
from dataNode import DataNode
from graphNode import GraphNode
from graphStructure import GraphStructure
import graphStructureConstructor
import json


def chainGraphFromJSON(inputJSON):
    inputObject = json.loads(inputJSON)
    graph = graphStructureConstructor.graphStructureFromJSON(json.dumps(inputObject["graph"]))
    chainGraph = ChainGraph(graph)
    return chainGraph


def chainGraphFromString(inputString):
    testDataGraphNodes = []
    previousNode = None
    for c in inputString:
        cDataType = DataType("char", lambda i: i == c)
        cDataNode = DataNode(cDataType, parsedData=c)
        cGraphNode = GraphNode(cDataNode)
        testDataGraphNodes.append(cGraphNode)
        if previousNode:
            previousNode.nexts.append(cGraphNode)
        previousNode = cGraphNode
    testDataGraphNodes[-1].nexts.append(None)

    testDataGraph = GraphStructure(testDataGraphNodes, "character_stream")
    return ChainGraph(testDataGraph)

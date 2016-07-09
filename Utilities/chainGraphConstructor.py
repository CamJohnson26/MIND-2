from chainGraph import ChainGraph
from graphNode import GraphNode
from graphStructure import GraphStructure
from Utilities.dataNodeConstructor import *
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
        cDataNode = loadDataNode("char.json")
        cDataNode.parsedData = c
        cGraphNode = GraphNode(cDataNode)
        testDataGraphNodes.append(cGraphNode)
        if previousNode:
            previousNode.nexts.append(cGraphNode)
        previousNode = cGraphNode
    testDataGraphNodes[-1].nexts.append(None)
    testDataGraph = GraphStructure(testDataGraphNodes, "character_stream")
    return ChainGraph(testDataGraph)

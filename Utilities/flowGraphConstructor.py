from flowGraph import FlowGraph
from guidMapper import GuidMapper
import graphStructureConstructor
import json


def flowGraphFromJSON(inputJSON, guidMapper=GuidMapper()):
    inputObject = json.loads(inputJSON)
    graph = graphStructureConstructor.graphStructureFromJSON(json.dumps(inputObject["graph"]), guidMapper=guidMapper)
    startNodes = []
    for node_id in inputObject["startNodes"]:
        for node in graph.nodes:
            if node.guid == guidMapper.get(node_id):
                startNodes.append(node)
    contextNodes = []
    for node_id in inputObject["contextNodes"]:
        for node in graph.nodes:
            if node.guid == guidMapper.get(node_id):
                contextNodes.append(node)
    flowGraph = FlowGraph(graph, startNodes, contextNodes=contextNodes)
    return flowGraph


def loadFlowGraph(inputFileName):
    f = open("Data/FlowGraphs/" + inputFileName)
    json = f.read()
    return flowGraphFromJSON(json)


def loadFlowGraphs(inputNames):
    rv = []
    for name in inputNames:
        rv.append(loadFlowGraph(name + ".json"))
    return rv

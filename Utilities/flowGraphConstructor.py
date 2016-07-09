from flowGraph import FlowGraph
import graphStructureConstructor
import graphNodeConstructor
import json


def flowGraphFromJSON(inputJSON):
    inputObject = json.loads(inputJSON)
    graph = graphStructureConstructor.graphStructureFromJSON(json.dumps(inputObject["graph"]))
    startNodes = []
    for node_id in inputObject["startNodes"]:
        for node in graph.nodes:
            if node.guid == node_id:
                startNodes.append(node)
    contextNodes = []
    for node_id in inputObject["contextNodes"]:
        for node in graph.nodes:
            if node.guid == node_id:
                contextNodes.append(node)
    flowGraph = FlowGraph(graph, startNodes, contextNodes=contextNodes)
    return flowGraph


def loadFlowGraph(inputFileName):
    f = open("Data/FlowGraphs/" + inputFileName)
    json = f.read()
    return flowGraphFromJSON(json)

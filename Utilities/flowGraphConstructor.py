from flowGraph import FlowGraph
from guidMapper import GuidMapper
import graphStructureConstructor
import json
import csv


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


def generateFlowGraphFiles(minFileName):
    with open("Data/FlowGraphs/" + minFileName) as minFile:
        inputValues = csv.reader(minFile, delimiter=",", quotechar="\'")
        for value in inputValues:
            new_json = {"class": "FlowGraph"}
            new_json["graph"] = {"nodes": [], "guid": -1, "class": "GraphStructure"}
            fileName = value[0]
            nodes = json.loads(value[1])
            for n in nodes:
                new_node = {"class": "GraphNode", "dataClass": None}
                new_node["guid"] = int(n[0])
                new_node["dataNode"] = n[1]
                new_node["dataClass"] = n[2]
                new_node["nexts"] = n[3]
                new_json["graph"]["nodes"].append(new_node)
            new_json["startNodes"] = json.loads(value[2])
            new_json["contextNodes"] = json.loads(value[3])
            new_json["graph"]["name"] = value[4]
            for key in new_json:
                if new_json[key] == "":
                    new_json[key] = None
            new_file = open("Data/FlowGraphs/" + fileName, 'w')
            new_file.write(json.dumps(new_json, indent=4))
            new_file.close()
    return json.dumps(new_json, indent=4)

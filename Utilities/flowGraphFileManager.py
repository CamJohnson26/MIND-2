from flowGraph import FlowGraph
from guidMapper import GuidMapper
from abstractFileManager import AbstractFileManager
from graphStructureConstructor import graphStructureFromJSON
import json


class FlowGraphFileManager(AbstractFileManager):

    def __init__(self):
        home_folder = "Data/FlowGraphs/"
        min_file_name = "flowGraphs.flowGraph"
        AbstractFileManager.__init__(self, home_folder, min_file_name)

    def objectFromJSON(self, inputJSON):
        gm = GuidMapper()

        inputObject = json.loads(inputJSON)
        graph = graphStructureFromJSON(json.dumps(inputObject["graph"]), guidMapper=gm)
        startNodes = []
        for node_id in inputObject["startNodes"]:
            for node in graph.nodes:
                if node.guid == gm.get(node_id):
                    startNodes.append(node)
        contextNodes = []
        for node_id in inputObject["contextNodes"]:
            for node in graph.nodes:
                if node.guid == gm.get(node_id):
                    contextNodes.append(node)
        flowGraph = FlowGraph(graph, startNodes, contextNodes=contextNodes)
        return flowGraph

    def min_file_to_json(self, minFile):
        value = self.min_file_to_array(minFile)
        new_json = {"class": "FlowGraph"}
        new_json["graph"] = {"nodes": [], "guid": -1, "class": "GraphStructure"}
        nodes = json.loads(value[1])
        for n in nodes:
            new_node = {"class": "GraphNode", "dataClass": None}
            new_node["guid"] = int(n[0])
            new_node["dataNode"] = n[1]
            new_node["dataClasses"] = n[2]
            new_node["nexts"] = n[3]
            new_json["graph"]["nodes"].append(new_node)
        new_json["startNodes"] = json.loads(value[2])
        new_json["contextNodes"] = json.loads(value[3])
        new_json["graph"]["name"] = value[4]
        for key in new_json:
            if new_json[key] == "":
                new_json[key] = None
        return json.dumps(new_json, indent=4)

    def json_to_min_file(self, inputJSON, fileLocation):
        rv = []
        j = json.loads(inputJSON)
        rv.append(fileLocation)

        newNodes = "["
        for i, n in enumerate(j["graph"]["nodes"]):
            newNodes += "["
            newNodes += str(i)
            newNodes += ","
            newNodes += "\"" + n["dataNode"] + "\"" if n["dataNode"] else "null"
            newNodes += ","
            newNodes += "{"
            for key in n["dataClasses"].keys():
                if n["dataClasses"][key]:
                    newNodes += "\"" + key + "\":\"" + n["dataClasses"][key] + "\","
                else:
                    newNodes += "\"" + key + "\":null,"
            if len(n["dataClasses"].keys()) > 0:
                newNodes = newNodes[:-1]
            newNodes += "}"
            newNodes += ","
            t = "["
            for k in n["nexts"]:
                if k:
                    t += str(k)
                else:
                    t += "null"
                t += ","
            if len(t) > 1:
                t = t[:-1]
            t += "]"
            newNodes += t
            newNodes += "]"
            newNodes += ","
        if len(newNodes) > 1:
            newNodes = newNodes[:-1]
        newNodes += "]"
        rv.append(newNodes)
        newNodes = "["
        for i, n in enumerate(j["startNodes"]):
            newNodes += str(i)
            newNodes += ","
        if len(newNodes) > 1:
            newNodes = newNodes[:-1]
        newNodes += "]"
        rv.append(newNodes)
        newNodes = "["
        for i, n in enumerate(j["contextNodes"]):
            newNodes += str(i)
            newNodes += ","
        if len(newNodes) > 1:
            newNodes = newNodes[:-1]
        newNodes += "]"
        rv.append(newNodes)
        rv.append(j["graph"]["name"])
        return self.array_to_min(rv)

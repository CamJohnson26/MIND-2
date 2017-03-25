from os import listdir, walk, path
from os.path import isfile, join
import csv
import json
from MIND2.flowGraph import FlowGraph
from MIND2.Utilities.guidMapper import GuidMapper
from MIND2.Utilities.constructors import graphFromJSON
from MIND2.dataClass import DataClass
from MIND2.dataType import DataType
import MIND2.Data.matchFunctions as matchFunctions


class FileManager:

    def __init__(self):
        self.flow_graph_home_folder = "Data/FlowGraphs/"
        self.flow_graph_min_file_name = "flowGraphs.flowGraph"
        self.data_class_home_folder = "Data/DataClasses/"
        self.data_class_min_file_name = "dataClasses.dataClass"
        self.data_type_home_folder = "Data/DataTypes/"
        self.data_type_min_file_name = "dataTypes.dataType"

    def load_flow_graph(self, input_file_name):
        f = open(join(self.flow_graph_home_folder, input_file_name))
        json = f.read()
        return self.flow_graph_object_from_json(json)

    def load_data_class(self, input_file_name):
        f = open(join(self.data_class_home_folder, input_file_name))
        json = f.read()
        return self.dataClassobjectFromJSON(json)

    def load_data_type(self, input_file_name):
        f = open(join(self.data_type_home_folder, input_file_name))
        json = f.read()
        return self.dataTypeobjectFromJSON(json)

    def load_flow_graphs(self, inputFolder):
        rv = []
        if type(inputFolder) is list:
            files = [str(f) + ".json" for f in inputFolder]
        else:
            path = join(self.flow_graph_home_folder, inputFolder)
            files = listdir(path)
            files = [join(inputFolder, f) for f in files if isfile(join(path, f))]
        for file in files:
            f = open(join(self.flow_graph_home_folder, file))
            json = f.read()
            rv.append(self.flow_graph_object_from_json(json))
        return rv

    def load_data_classes(self, inputFolder):
        rv = []
        if type(inputFolder) is list:
            files = [str(f) + ".json" for f in inputFolder]
        else:
            path = join(self.data_class_home_folder, inputFolder)
            files = listdir(path)
            files = [join(inputFolder, f) for f in files if isfile(join(path, f))]
        for file in files:
            f = open(join(self.data_class_home_folder, file))
            json = f.read()
            rv.append(self.dataClassobjectFromJSON(json))
        return rv

    def load_data_types(self, inputFolder):
        rv = []
        if type(inputFolder) is list:
            files = [str(f) + ".json" for f in inputFolder]
        else:
            path = join(self.data_type_home_folder, inputFolder)
            files = listdir(path)
            files = [join(inputFolder, f) for f in files if isfile(join(path, f))]
        for file in files:
            f = open(join(self.data_type_home_folder, file))
            json = f.read()
            rv.append(self.dataTypeobjectFromJSON(json))
        return rv

    def generateFiles(self, home_folder, min_file_name, min_file_to_json):
        with open(join(home_folder, min_file_name)) as minFile:
            lines = minFile.readlines()
            for line in lines:
                new_json = min_file_to_json(line)
                fileName = self.min_file_to_array(line)[0]
                new_file = open(fileName, 'w')
                new_file.write(new_json)
                new_file.close()

    def refreshObjects(self, home_folder, min_file_name, json_to_min_file, min_file_to_json):
        self.save_home_folder_to_min_file(home_folder, min_file_name, json_to_min_file)
        self.generateFiles(home_folder, min_file_name, min_file_to_json)

    def add_minObject_to_file(self, minObject, home_folder, min_file_name):
        with open(join(home_folder, min_file_name), 'a') as minFile:
            minFile.write(minObject + "\n")

    @staticmethod
    def min_file_to_array(minFile):
        return list(csv.reader([minFile], delimiter=",", quotechar="'"))[0]

    @staticmethod
    def array_to_min(iarray):
        rString = ""
        for i in iarray:
            if type(i) is str:
                rString += "\'" + i + "\'"
            elif type(i) is list:
                rString += ("[" + ",".join([dc for dc in i]) + "]")
            elif type(i) is dict:
                rString += "'{"
                for key in i.keys():
                    if not i[key]:
                        rString += "\"" + key + "\": null,"
                    else:
                        rString += "\"" + key + "\":\"" + i[key] + "\","
                if len(i.keys()) > 0:
                    rString = rString[:-1]
                rString += "}'"
            elif type(i) is int:
                rString += str(i)
            elif not i:
                pass
            else:
                rString += str(i)
            rString += ","

        if len(rString) > 0:
            rString = rString[:-1]
        return rString

    def save_home_folder_to_min_file(self, home_folder, min_file_name, json_to_min_file):
        folder = ""
        minFile = ""
        for subdir, dirs, files in walk(join(home_folder, folder)):
            for file in files:
                file = path.join(subdir, file)
                file = file.replace("\\", "/")
                if (file.endswith("json")):
                    with open(file, 'r') as f:
                        minFile += json_to_min_file(f.read(), file)
                        minFile += "\n"
        for m in minFile.split("\n"):
            self.add_minObject_to_file(m, home_folder, min_file_name)
        self.dedup_min_file(minFile, home_folder, min_file_name)

    def dedup_min_file(self, tempMin, home_folder, min_file_name):
        fileLocation = join(home_folder, min_file_name)
        tempMinList = tempMin.split("\n")
        try:
            tempMinList.remove("\n")
        except ValueError:
            pass
        lines = set(tempMinList)
        with open(fileLocation) as oldMin:
            t = oldMin.read().split("\n")
            try:
                t.remove("\n")
            except ValueError:
                pass
            lines |= set(t)
        new_lines = {}
        for line in lines:
            lineKey = line.split(",")[0]
            try:
                cur_line = new_lines[lineKey]
            except KeyError:
                cur_line = ""
            if len(line) > len(cur_line):
                new_lines[lineKey] = line
        result = list(new_lines.values())
        result.sort()
        try:
            result.remove("")
        except ValueError:
            pass
        with open(fileLocation, 'r+') as oldMin:
            oldMin.writelines("\n".join(result) + "\n")
            oldMin.truncate()

    def flow_graph_object_from_json(self, inputJSON):
        gm = GuidMapper()

        inputObject = json.loads(inputJSON)
        nodes, name = graphFromJSON(json.dumps(inputObject["graph"]), guidMapper=gm)
        startNodes = []
        for node_id in inputObject["startNodes"]:
            for node in nodes:
                if node.guid == gm.get(node_id):
                    startNodes.append(node)
        contextNodes = []
        for node_id in inputObject["contextNodes"]:
            for node in nodes:
                if node.guid == gm.get(node_id):
                    contextNodes.append(node)
        flowGraph = FlowGraph(nodes, name, startNodes, contextNodes=contextNodes)
        return flowGraph

    def flow_graph_min_file_to_json(self, minFile):
        value = self.min_file_to_array(minFile)
        new_json = {"class": "FlowGraph"}
        new_json["graph"] = {"nodes": [], "guid": -1, "class": "GraphStructure"}
        nodes = json.loads(value[1])
        for n in nodes:
            new_node = {"class": "GraphNode", "dataClass": None}
            new_node["guid"] = int(n[0])
            new_node["dataType"] = n[1]
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

    def flow_graph_json_to_min_file(self, inputJSON, fileLocation):
        rv = []
        j = json.loads(inputJSON)
        rv.append(fileLocation)

        newNodes = "["
        for i, n in enumerate(j["graph"]["nodes"]):
            newNodes += "["
            newNodes += str(i)
            newNodes += ","
            newNodes += "\"" + n["dataType"] + "\"" if n["dataType"] else "null"
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
            newNodes += str(n)
            newNodes += ","
        if len(newNodes) > 1:
            newNodes = newNodes[:-1]
        newNodes += "]"
        rv.append(newNodes)
        rv.append(j["graph"]["name"])
        return self.array_to_min(rv)


    def dataClassobjectFromJSON(self, inputJSON):
        inputObject = json.loads(inputJSON)
        if not inputObject["flowGraph"]:
            flowGraph = None
        elif type(inputObject["flowGraph"] is str):
            flowGraph = self.load_flow_graph(inputObject["flowGraph"])
        else:
            flowGraph = self.flow_graph_object_from_json(json.dumps(inputObject["flowGraph"]))
        dataClassIndex = inputObject["dataClassIndex"]
        dataClassString = inputObject["dataClassString"]
        dataClasses = inputObject["dataClasses"]
        dataClass = DataClass(flowGraph, dataClassIndex, dataClassString)
        for key in dataClasses.keys():
            dataClasses[key] = self.load_data_class(dataClasses[key])
        dataClass.dataClasses = dataClasses
        return dataClass

    def data_class_min_file_to_json(self, minFile):
        value = self.min_file_to_array(minFile)
        new_json = {"class": "DataClass"}
        new_json["dataClassIndex"] = int(value[1])
        new_json["dataClassString"] = value[2]
        new_json["flowGraph"] = value[3]
        new_json["dataClasses"] = json.loads(value[4])
        for key in new_json:
            if new_json[key] == "":
                new_json[key] = None
        return json.dumps(new_json, indent=4)

    def data_class_json_to_min_file(self, inputJSON, fileLocation):
        rv = []
        j = json.loads(inputJSON)
        rv.append(fileLocation)
        rv.append(j["dataClassIndex"])
        rv.append(j["dataClassString"])
        rv.append(j["flowGraph"])
        rv.append(j["dataClasses"])
        return self.array_to_min(rv)

    def data_class_get_next_index(self):
        with open(join(self.data_class_home_folder, self.data_class_min_file_name)) as minFile:
            lines = minFile.read().split("\n")
            indexes = [a.split(",")[1] for a in lines if a != ""]
            return int(max(indexes)) + 1

    def dataTypeobjectFromJSON(self, inputJSON):
        inputObject = json.loads(inputJSON)
        dataTypeName = inputObject["dataTypeName"]
        dataClasses = inputObject["dataClasses"]
        matchFunction = getattr(matchFunctions, inputObject["matchFunction"])
        dataType = DataType(dataTypeName, dataClasses, matchFunction)
        return dataType

    def data_type_min_file_to_json(self, minFile):
        value = self.min_file_to_array(minFile)
        new_json = {"class": "DataType"}
        new_json["dataTypeName"] = value[1]
        new_json["dataClasses"] = json.loads(value[2])
        new_json["matchFunction"] = value[3]
        for key in new_json:
            if new_json[key] == "":
                new_json[key] = None
        return json.dumps(new_json, indent=4)

    def data_type_json_to_min_file(self, inputJSON, fileLocation):
        rv = []
        j = json.loads(inputJSON)
        rv.append(fileLocation)
        rv.append(j["dataTypeName"])
        rv.append(j["dataClasses"])
        rv.append(j["matchFunction"])

        return self.array_to_min(rv)
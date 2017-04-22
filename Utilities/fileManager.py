from os import listdir, walk, path, makedirs
from os.path import isfile, join, isdir
import csv
import json
from MIND2.flowGraph import FlowGraph
from MIND2.Utilities.guidMapper import GuidMapper
from MIND2.Utilities.constructors import graphFromJSON
from MIND2.Utilities.constructors import graphFromJSON_old
from MIND2.dataClass import DataClass
from MIND2.dataType import DataType
import MIND2.Data.matchFunctions_old as matchFunctions


class FileManager:

    def __init__(self):
        self.flow_graph_home_folder = "Data/FlowGraphs/"
        self.flow_graph_min_file_name = "flowGraphs.flowGraph"
        self.data_class_home_folder = "Data/DataClasses/"
        self.data_class_min_file_name = "dataClasses.dataClass"
        self.data_type_home_folder = "Data/DataTypes/"
        self.data_type_min_file_name = "dataTypes.dataType"

    def load_package(self, package_name):
        package_folder = join("Data", package_name)
        level_folders = [f for f in listdir(package_folder) if not isfile(f)]
        levels = []
        data_types = {}
        for level_folder in level_folders:
            level = self.load_level(level_folder, join("Data", package_name), data_types)
            for key in level:
                data_types[key] = level[key]
            levels.append(level)
        return levels

    def load_level(self, level_folder, root, low_level_data_types):
        data_type_folders = [f for f in listdir(join(root, level_folder)) if not isfile(f)]
        data_types = {}
        flow_graphs = {}
        for data_type_folder in data_type_folders:
            data_types[data_type_folder] = self.load_data_type_new(data_type_folder, join(root, level_folder))
        for key in data_types:
            low_level_data_types[key] = data_types[key]
        for data_type_folder in data_type_folders:
            flow_graphs[data_type_folder] = self.load_flow_graph_new("flow_graph.json", join(root, level_folder, data_type_folder), low_level_data_types)
        #print("\n")
        #print([(a, data_types[a]) for a in data_types])
        #print([flow_graphs[a] for a in flow_graphs])
        return data_types

    def load_data_type_new(self, data_type_folder, root):
        data_class_types_path = join(root, data_type_folder, "classes")
        try:
            data_class_types = [f for f in listdir(data_class_types_path) if not isfile(f)]
        except FileNotFoundError:
            data_class_types = []
        classes = {}
        for data_class_type in data_class_types:
            classes[data_class_type] = self.load_data_class_type(data_class_type, data_class_types_path)
        match_function_name = "alwaysFalse"
        data_type_name = data_type_folder
        match_function = getattr(matchFunctions, match_function_name)
        return DataType(data_type_name, classes, match_function)

    def load_flow_graph_new(self, flow_graph_file, root, low_level_data_types):
        try:
            flow_graph_json = open(join(root, flow_graph_file)).read()
            return self.flow_graph_object_from_json(flow_graph_json, low_level_data_types)
        except FileNotFoundError:
            return None

    def load_data_class_type(self, data_class_type, root):
        data_class_folders_path = join(root, data_class_type)
        data_class_folders = [f for f in listdir(data_class_folders_path) if not isfile(f)]
        data_classes = {}
        for data_class_folder in data_class_folders:
            data_classes[data_class_folder.split(" - ")[1]] = self.load_data_class_new(data_class_folder, data_class_folders_path)
        return data_classes

    def load_data_class_new(self, data_class_folder, root):
        data_class_json = json.loads(open(join(root, data_class_folder, "data_class.json")).read())
        #flow_graph = self.load_flow_graph(join(root, data_class_folder, "flow_graph.json"))
        flow_graph = None
        data_class_index = int(data_class_folder.split(" - ")[0])
        data_class_name = data_class_json["dataClassString"]
        return DataClass(flow_graph, data_class_index, data_class_name)

    def load_flow_graph(self, input_file_name):
        f = open(join(self.flow_graph_home_folder, input_file_name))
        json = f.read()
        return self.flow_graph_object_from_json(json)

    def load_flow_graph_old(self, input_file_name):
        f = open(join(self.flow_graph_home_folder, input_file_name))
        json = f.read()
        return self.flow_graph_object_from_json_old(json)

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
            rv.append(self.flow_graph_object_from_json_old(json))
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

    def load_data_classes_old(self, inputFolder):
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
            rv.append(self.dataClassobjectFromJSON_old(json))
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

    def create_min_files(self, root):
        for subdir, dirs, files in walk(root):
            for dir in dirs:
                if dir == "classes":
                    self.data_class_folder_to_min(join(subdir, dir))

    def data_class_folder_to_min(self, folder):
        min_file = open(join(folder, "min_file.csv"), 'w')
        lines = []
        for dir in listdir(folder):
            if isdir(join(folder, dir)):
                for subdir in listdir(join(folder, dir)):
                    index = subdir.split(" - ")[0]
                    name = path.split(folder)[-1] + "/" + subdir.split(" - ")[1]
                    try:
                        flow_graph_json = open(join(folder, dir, subdir, "flow_graph.json")).read()
                    except FileNotFoundError:
                        flow_graph_json = None
                    flow_graph = self.flow_graph_json_to_min_file(flow_graph_json, name)#, index)
                    lines.append(flow_graph)
        min_file.write("\n".join(lines))
        min_file.close()

    def generate_min_files(self, root):
        for subdir, dirs, files in walk(root):
            for file in files:
                if file == "min_file.csv":
                    self.generate_flow_graphs_from_min_file_folder(file, subdir)

    def generateFiles(self, home_folder, min_file_name, min_file_to_json):
        with open(join(home_folder, min_file_name)) as minFile:
            lines = minFile.readlines()
            for line in lines:
                print(line)
                new_json = min_file_to_json(line)
                fileName = self.min_file_to_array(line)[0]
                new_file = open(fileName, 'w')
                new_file.write(new_json)
                new_file.close()

    def generate_flow_graphs_from_min_file_folder(self, min_file_name, root):
        try:
            min_file = open(join(root, min_file_name), 'r')
            f = self.flow_graph_min_file_to_json(min_file)
            for key in f:
                try:
                    makedirs(join(root, key))
                except FileExistsError:
                    pass
                if f[key]:
                    file = open(join(root, key, "flow_graph.json"), 'w')
                    file.write(f[key])
                    file.close()
        except FileNotFoundError:
            pass

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

    def flow_graph_object_from_json_old(self, inputJSON):
        gm = GuidMapper()

        inputObject = json.loads(inputJSON)
        nodes, name = graphFromJSON_old(json.dumps(inputObject["graph"]), guidMapper=gm)
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

    def flow_graph_object_from_json_new(self, inputJSON, low_level_data_types):
        gm = GuidMapper()

        inputObject = json.loads(inputJSON)
        nodes, name = graphFromJSON(json.dumps(inputObject["graph"]), low_level_data_types, guidMapper=gm)
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

    def flow_graph_min_file_to_json_new(self, minFile):
        ret_json = {}
        values = self.min_file_to_array(minFile)
        for value in values:
            if len(value) > 2:
                new_json = {"class": "FlowGraph"}
                new_json["graph"] = {"nodes": [], "guid": -1, "class": "GraphStructure"}
                nodes = json.loads(value[2])
                for n in nodes:
                    new_node = {"class": "GraphNode", "dataClass": None}
                    new_node["guid"] = int(n[0])
                    new_node["dataType"] = n[1]
                    new_node["dataClasses"] = n[2]
                    new_node["nexts"] = n[3]
                    new_json["graph"]["nodes"].append(new_node)
                new_json["startNodes"] = json.loads(value[3])
                new_json["contextNodes"] = json.loads(value[4])
                new_json["dataClasses"] = json.loads(value[6])
                new_json["graph"]["name"] = value[5]
                for key in new_json:
                    if new_json[key] == "":
                        new_json[key] = None
                new_json = json.dumps(new_json, indent=4)
            else:
                new_json = None
            file_path = value[1].split("/")
            file_path[-1] = str(value[0]) + " - " + file_path[-1]
            file_path = "/".join(file_path)
            ret_json[file_path] = new_json
        return ret_json

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
        new_json = json.dumps(new_json, indent=4)
        file_path = value[1].split("/")
        file_path[-1] = str(value[0]) + " - " + file_path[-1]
        file_path = "/".join(file_path)
        return new_json

    def flow_graph_json_to_min_file(self, inputJSON, name):
        rv = []
        rv.append(name)

        if not inputJSON:
            return self.array_to_min(rv)

        j = json.loads(inputJSON)
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
        rv.append(newNodes)
        return self.array_to_min(rv)


    def flow_graph_json_to_min_file_new(self, inputJSON, name):
        rv = []
        rv.append(name)

        if not inputJSON:
            return self.array_to_min(rv)

        j = json.loads(inputJSON)
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
        newNodes = "{"
        for key in j["dataClasses"].keys():
            if j["dataClasses"][key]:
                newNodes += "\"" + key + "\":\"" + j["dataClasses"][key] + "\","
            else:
                newNodes += "\"" + key + "\":null,"
        if len(j["dataClasses"].keys()) > 0:
            newNodes = newNodes[:-1]
        newNodes += "}"
        rv.append(newNodes)
        return self.array_to_min(rv)

    def dataClassobjectFromJSON(self, inputJSON):
        inputObject = json.loads(inputJSON)
        if not inputObject["flowGraph"]:
            flowGraph = None
        elif type(inputObject["flowGraph"] is str):
            flowGraph = self.load_flow_graph_old(inputObject["flowGraph"])
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

    def dataClassobjectFromJSON_old(self, inputJSON):
        inputObject = json.loads(inputJSON)
        if not inputObject["flowGraph"]:
            flowGraph = None
        elif type(inputObject["flowGraph"] is str):
            flowGraph = self.load_flow_graph_old(inputObject["flowGraph"])
        else:
            flowGraph = self.flow_graph_object_from_json_old(json.dumps(inputObject["flowGraph"]))
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
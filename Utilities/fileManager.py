from os import listdir, walk, path, makedirs
from os.path import isfile, join, isdir
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
            data_types[data_type_folder] = self.load_data_type(data_type_folder, join(root, level_folder), low_level_data_types=low_level_data_types)
        for key in data_types:
            low_level_data_types[key] = data_types[key]
        for data_type_folder in data_type_folders:
            flow_graphs[data_type_folder] = self.load_flow_graph("flow_graph.json", join(root, level_folder, data_type_folder), low_level_data_types)
        return data_types

    def load_data_type(self, data_type_folder, root, low_level_data_types=None):
        if not low_level_data_types:
            low_level_data_types = {}
        data_class_types_path = join(root, data_type_folder, "classes")
        try:
            data_class_types = [f for f in listdir(data_class_types_path) if not isfile(join(data_class_types_path, f))]
        except FileNotFoundError:
            data_class_types = []
        classes = {}
        for data_class_type in data_class_types:
            classes[data_class_type] = self.load_data_class_type(data_class_type, data_class_types_path, low_level_data_types)
        data_type_name = data_type_folder
        try:
            match_function = getattr(matchFunctions, data_type_name)
        except AttributeError:
            match_function = getattr(matchFunctions, "alwaysFalse")
        return DataType(data_type_name, classes, match_function)

    def load_flow_graph(self, flow_graph_file, root, low_level_data_types):
        try:
            flow_graph_json = open(join(root, flow_graph_file)).read()
            return self.flow_graph_object_from_json(flow_graph_json, low_level_data_types)
        except FileNotFoundError:
            return None

    def load_data_class_type(self, data_class_type, root, low_level_data_types):
        data_class_folders_path = join(root, data_class_type)
        data_class_folders = [f for f in listdir(data_class_folders_path) if not isfile(f)]
        data_classes = {}
        for data_class_folder in data_class_folders:
            data_classes[data_class_folder.split(" - ")[1]] = self.load_data_class(data_class_folder, data_class_folders_path, low_level_data_types)
        return data_classes

    def load_data_class(self, data_class_folder, root, low_level_data_types):
        try:
            flow_graph = self.load_flow_graph("flow_graph.json", join(root, data_class_folder), low_level_data_types)
            data_classes = self.load_data_classes_from_flow_graph(join(root, data_class_folder, "flow_graph.json"), low_level_data_types)
        except FileNotFoundError:
            flow_graph = None
            data_classes = {}
        data_class_index = int(data_class_folder.split(" - ")[0])
        data_class_name = data_class_folder.split(" - ")[1]
        data_class = DataClass(flow_graph, data_class_index, data_class_name)
        data_class.dataClasses = data_classes
        return data_class

    def load_data_classes_from_flow_graph(self, input_file_name, low_level_data_types):
        f = open(input_file_name)
        j = json.loads(f.read())
        data_classes = j.get("dataClasses", {});
        root = path.join(input_file_name, "..\\..\\..")
        rv = {}
        for data_class_type in data_classes.keys():
            rv[data_class_type] = self.load_data_class(data_classes[data_class_type], root, low_level_data_types)
        return rv

    def load_flow_graphs(self, inputFolder, root, low_level_data_types={}):
        rv = []
        if type(inputFolder) is list:
            files = [join(f, "flow_graph.json") for f in inputFolder]
        else:
            path = join(root, inputFolder)
            files = listdir(path)
            files = [join(inputFolder, f) for f in files if isfile(join(path, f))]
        for file in files:
            f = open(join(root, file))
            json = f.read()
            rv.append(self.flow_graph_object_from_json(json, low_level_data_types))
        return rv

    def flow_graph_object_from_json(self, inputJSON, low_level_data_types):
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

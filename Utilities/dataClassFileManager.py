from dataClass import DataClass
from Utilities.abstractFileManager import AbstractFileManager
from Utilities.flowGraphFileManager import FlowGraphFileManager
import json
from os.path import join


class DataClassFileManager(AbstractFileManager):

    def __init__(self):
        home_folder = "Data/DataClasses/"
        min_file_name = "dataClasses.dataClass"
        AbstractFileManager.__init__(self, home_folder, min_file_name)

    def objectFromJSON(self, inputJSON):
        inputObject = json.loads(inputJSON)
        fgfm = FlowGraphFileManager()
        if not inputObject["flowGraph"]:
            flowGraph = None
        elif type(inputObject["flowGraph"] is str):
            flowGraph = fgfm.loadObject(inputObject["flowGraph"])
        else:
            flowGraph = fgfm.objectFromJSON(json.dumps(inputObject["flowGraph"]))
        dataClassIndex = inputObject["dataClassIndex"]
        dataClassString = inputObject["dataClassString"]
        dataClasses = inputObject["dataClasses"]
        dataClass = DataClass(flowGraph, dataClassIndex, dataClassString)
        for key in dataClasses.keys():
            dataClasses[key] = self.loadObject(dataClasses[key])
        dataClass.dataClasses = dataClasses
        return dataClass

    def min_file_to_json(self, minFile):
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

    def json_to_min_file(self, inputJSON, fileLocation):
        rv = []
        j = json.loads(inputJSON)
        rv.append(fileLocation)
        rv.append(j["dataClassIndex"])
        rv.append(j["dataClassString"])
        rv.append(j["flowGraph"])
        rv.append(j["dataClasses"])
        return self.array_to_min(rv)

    def get_next_index(self):
        with open(join(self.home_folder, self.min_file_name)) as minFile:
            lines = minFile.read().split("\n")
            indexes = [a.split(",")[1] for a in lines if a != ""]
            return int(max(indexes)) + 1

from dataNode import DataNode
from abstractFileManager import AbstractFileManager
from dataTypeFileManager import DataTypeFileManager
import json


class DataNodeFileManager(AbstractFileManager):

    def __init__(self):
        home_folder = "Data/DataNodes/"
        min_file_name = "dataNodes.dataNode"
        AbstractFileManager.__init__(self, home_folder, min_file_name)

    def objectFromJSON(self, inputJSON):
        inputObject = json.loads(inputJSON)
        dtfm = DataTypeFileManager()
        if type(inputObject["dataType"]) in [unicode, str]:
            dataType = dtfm.loadObject(inputObject["dataType"])
        else:
            dataType = dtfm.objectFromJSON(json.dumps(inputObject["dataType"]))
        dataNode = DataNode(dataType)
        dataNode.parsedData = inputObject["parsedData"]
        return dataNode

    def min_file_to_json(self, minFile):
        value = self.min_file_to_array(minFile)
        new_json = {"class": "DataNode"}
        new_json["dataType"] = value[1]
        new_json["dataClasses"] = json.loads(value[2])
        new_json["parsedData"] = value[3]
        for key in new_json:
            if new_json[key] == "":
                new_json[key] = None
        return json.dumps(new_json, indent=4)

    def json_to_min_file(self, inputJSON, fileLocation):
        rv = []
        j = json.loads(inputJSON)
        rv.append(fileLocation)
        rv.append(j["dataType"])
        rv.append(j["dataClasses"])
        rv.append(j["parsedData"])
        return self.array_to_min(rv)

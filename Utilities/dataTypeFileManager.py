from dataType import DataType
from abstractFileManager import AbstractFileManager
import json
import Data.matchFunctions as matchFunctions


class DataTypeFileManager(AbstractFileManager):

    def __init__(self):
        home_folder = "Data/DataTypes/"
        min_file_name = "dataTypes.dataType"
        AbstractFileManager.__init__(self, home_folder, min_file_name)

    def objectFromJSON(self, inputJSON):
        inputObject = json.loads(inputJSON)
        dataTypeName = inputObject["dataTypeName"]
        dataClasses = inputObject["dataClasses"]
        matchFunction = getattr(matchFunctions, inputObject["matchFunction"])
        dataType = DataType(dataTypeName, dataClasses, matchFunction)
        return dataType

    def min_file_to_json(self, minFile):
        value = self.min_file_to_array(minFile)
        new_json = {"class": "DataType"}
        new_json["dataTypeName"] = value[1]
        new_json["dataClasses"] = json.loads(value[2])
        new_json["matchFunction"] = value[3]
        for key in new_json:
            if new_json[key] == "":
                new_json[key] = None
        return json.dumps(new_json, indent=4)

    def json_to_min_file(self, inputJSON, fileLocation):
        rv = []
        j = json.loads(inputJSON)
        rv.append(fileLocation)
        rv.append(j["dataTypeName"])
        rv.append(j["dataClasses"])
        rv.append(j["matchFunction"])

        return self.array_to_min(rv)

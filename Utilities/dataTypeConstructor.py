from dataType import DataType
import dataClassConstructor
import Data.matchFunctions as matchFunctions
import csv
import json


def dataTypeFromJSON(inputJSON):
    inputObject = json.loads(inputJSON)
    dataTypeName = inputObject["dataTypeName"]
    matchFunction = getattr(matchFunctions, inputObject["matchFunction"])
    dataType = DataType(dataTypeName, matchFunction)
    return dataType


def loadDataType(inputFileName):
    f = open("Data/DataTypes/" + inputFileName)
    json = f.read()
    return dataTypeFromJSON(json)


def generateDataTypeFiles(minFileName):
    new_json = {"class": "DataType"}
    with open("Data/DataTypes/" + minFileName) as minFile:
        inputValues = csv.reader(minFile, delimiter=",", quotechar="\"")
        for value in inputValues:
            fileName = value[0]
            new_json["dataTypeName"] = value[1]
            new_json["matchFunction"] = value[2]
            for key in new_json:
                if new_json[key] == "":
                    new_json[key] = None
            new_file = open("Data/DataTypes/" + fileName, 'w')
            new_file.write(json.dumps(new_json, indent=4))
            new_file.close()
    return json.dumps(new_json, indent=4)

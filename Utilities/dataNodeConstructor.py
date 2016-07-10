from dataNode import DataNode
import dataTypeConstructor
import json
import csv


def dataNodeFromJSON(inputJSON):
    inputObject = json.loads(inputJSON)
    if type(inputObject["dataType"]) is unicode:
        dataType = dataTypeConstructor.loadDataType(inputObject["dataType"])
    else:
        dataType = dataTypeConstructor.dataTypeFromJSON(json.dumps(inputObject["dataType"]))
    dataNode = DataNode(dataType)
    dataNode.parsedData = inputObject["parsedData"]
    return dataNode


def loadDataNode(inputFileName):
    f = open("Data/DataNodes/" + inputFileName)
    json = f.read()
    return dataNodeFromJSON(json)


def generateDataNodeFiles(minFileName):
    new_json = {"class": "DataNode"}
    with open("Data/DataNodes/" + minFileName) as minFile:
        inputValues = csv.reader(minFile, delimiter=",", quotechar="\"")
        for value in inputValues:
            fileName = value[0]
            new_json["dataType"] = value[1]
            new_json["parsedData"] = value[2]
            new_json["dataClass"] = value[3]
            for key in new_json:
                if new_json[key] == "":
                    new_json[key] = None
            new_file = open("Data/DataNodes/" + fileName, 'w')
            new_file.write(json.dumps(new_json, indent=4))
            new_file.close()
    return json.dumps(new_json, indent=4)

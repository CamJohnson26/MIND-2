from dataNode import DataNode
import dataTypeConstructor
import json


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

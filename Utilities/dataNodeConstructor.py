from dataNode import DataNode
import dataTypeConstructor
import dataClassConstructor
import json


def dataNodeFromJSON(inputJSON):
    inputObject = json.loads(inputJSON)
    if type(inputObject["dataType"]) is unicode:
        dataType = dataTypeConstructor.loadDataType(inputObject["dataType"])
    else:
        dataType = dataTypeConstructor.dataTypeFromJSON(json.dumps(inputObject["dataType"]))
    if inputObject["dataClass"] is None:
    	dataClass = None
    else:
        dataClass = dataClassConstructor.dataClassFromJSON(json.dumps(inputObject["dataClass"]))
    dataNode = DataNode(dataType)
    dataNode.parsedData = inputObject["parsedData"]
    dataNode.dataClass = dataClass
    return dataNode

def loadDataNode(inputFileName):
    f = open("Data/DataNodes/" + inputFileName)
    json = f.read()
    return dataNodeFromJSON(json)

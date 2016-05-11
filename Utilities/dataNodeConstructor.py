from dataNode import DataNode
import dataTypeConstructor
import dataClassConstructor
import json


def dataNodeFromJSON(inputJSON):
    inputObject = json.loads(inputJSON)
    dataType = dataTypeConstructor.dataTypeFromJSON(json.dumps(inputObject["dataType"]))
    if inputObject["dataClass"] is None:
    	dataClass = None
    else:
        dataClass = dataClassConstructor.dataClassFromJSON(json.dumps(inputObject["dataClass"]))
    dataNode = DataNode(dataType)
    dataNode.parsedData = inputObject["parsedData"]
    dataNode.dataClass = dataClass
    return dataNode

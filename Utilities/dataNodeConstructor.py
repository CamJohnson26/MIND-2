from dataNode import DataNode
import dataTypeConstructor
import json


def dataNodeFromJSON(inputJSON):
    inputObject = json.loads(inputJSON)
    dataType = dataTypeConstructor.dataTypeFromJSON(json.dumps(inputObject["dataType"]))
    dataNode = DataNode(dataType)
    dataNode.parsedData = inputObject["parsedData"]
    return dataNode

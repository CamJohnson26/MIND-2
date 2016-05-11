from dataClass import DataClass
import flowGraphConstructor
import json


def dataClassFromJSON(inputJSON):
    inputObject = json.loads(inputJSON)
    flowGraph = flowGraphConstructor.flowGraphFromJSON(json.dumps(inputObject["flowGraph"]))
    dataClassIndex = inputObject["dataClassIndex"]
    dataClassString = inputObject["dataClassString"]
    dataClass = DataClass(flowGraph, dataClassIndex, dataClassString)
    return dataClass

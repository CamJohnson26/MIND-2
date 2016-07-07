from dataClass import DataClass
from flowGraphConstructor import *
import json


def dataClassFromJSON(inputJSON):
    inputObject = json.loads(inputJSON)
    if type(inputObject["flowGraph"] is unicode):
        flowGraph = loadFlowGraph(inputObject["flowGraph"])
    else:
        flowGraph = flowGraphFromJSON(json.dumps(inputObject["flowGraph"]))
    dataClassIndex = inputObject["dataClassIndex"]
    dataClassString = inputObject["dataClassString"]
    dataClass = DataClass(flowGraph, dataClassIndex, dataClassString)
    return dataClass


def loadDataClass(inputFileName):
    f = open("Data/DataClasses/" + inputFileName)
    json = f.read()
    return dataClassFromJSON(json)


def loadDataClasses(inputFileNames):
    rv = []
    for inputFileName in inputFileNames:
        f = open("Data/DataClasses/" + inputFileName)
        json = f.read()
        rv.append(dataClassFromJSON(json))
    return rv

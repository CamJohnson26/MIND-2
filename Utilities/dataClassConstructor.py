from dataClass import DataClass
from flowGraphConstructor import *
from os import listdir
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


def loadDataClasses(inputFolder):
    rv = []
    if type(inputFolder) is list:
        files = [str(f) + ".json" for f in inputFolder]
    else:
        files = listdir("Data/DataClasses/" + inputFolder)
        files = [inputFolder + "/" + f for f in files]
    for file in files:
        f = open("Data/DataClasses/" + file)
        json = f.read()
        rv.append(dataClassFromJSON(json))
    return rv

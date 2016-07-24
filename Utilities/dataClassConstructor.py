from dataClass import DataClass
from flowGraphConstructor import *
from os import listdir
from os.path import isfile, join
import json
import csv


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
        path = "Data/DataClasses/" + inputFolder
        files = listdir(path)
        files = [inputFolder + "/" + f for f in files if isfile(join(path, f))]
    for file in files:
        f = open("Data/DataClasses/" + file)
        json = f.read()
        rv.append(dataClassFromJSON(json))
    return rv


def generateDataClassFiles(minFileName):
    new_json = {"class": "DataClass"}
    with open("Data/DataClasses/" + minFileName) as minFile:
        inputValues = csv.reader(minFile, delimiter=",", quotechar="\"")
        for value in inputValues:
            fileName = value[0]
            new_json["dataClassIndex"] = int(value[1])
            new_json["dataClassString"] = value[2]
            new_json["flowGraph"] = value[3]
            for key in new_json:
                if new_json[key] == "":
                    new_json[key] = None
            new_file = open("Data/DataClasses/" + fileName, 'w')
            new_file.write(json.dumps(new_json, indent=4))
            new_file.close()
    return json.dumps(new_json, indent=4)

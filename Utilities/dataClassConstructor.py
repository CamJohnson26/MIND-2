from dataClass import DataClass
from flowGraphConstructor import *
from os import listdir, walk, path
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
    dataClasses = inputObject["dataClasses"]
    dataClass = DataClass(flowGraph, dataClassIndex, dataClassString)
    dataClass.dataClasses = dataClasses
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
        inputValues = csv.reader(minFile, delimiter=",", quotechar="\'")
        for value in inputValues:
            fileName = value[0]
            new_json["dataClassIndex"] = int(value[1])
            new_json["dataClassString"] = value[2]
            new_json["flowGraph"] = value[3]
            new_json["dataClasses"] = json.loads(value[4])
            for key in new_json:
                if new_json[key] == "":
                    new_json[key] = None
            new_file = open(fileName, 'w')
            new_file.write(json.dumps(new_json, indent=4))
            new_file.close()
    return json.dumps(new_json, indent=4)


def generateDataClassMinFile(inputJSON, fileLocation):
    rv = []
    j = json.loads(inputJSON)
    rv.append(fileLocation)
    rv.append(j["dataClassIndex"])
    rv.append(j["dataClassString"])
    rv.append(j["flowGraph"])
    rv.append(j["dataClasses"])

    rString = ""
    for i in rv:
        if type(i) is unicode or type(i) is str:
            rString += "\"" + i + "\""
        elif i is None:
            pass
        elif type(i) is dict:
            rString += "{"
            for key in i.keys():
                rString += "\"" + key + "\":\"" + i[key] + "\","
            if len(i.keys()) > 0:
                rString = rString[:-1]
            rString += "}"
        else:
            rString += str(i)
        rString += ","

    if len(rString) > 0:
        rString = rString[:-1]
    return rString


def saveDataClassFolderToMinFile(folderName):
    minFile = ""
    for subdir, dirs, files in walk(folderName):
        for file in files:
            file = path.join(subdir, file)
            file = file.replace("\\","/")
            if (file.endswith("json")):
                with open(file, 'r') as f:
                    minFile += generateDataClassMinFile(f.read(), file)
                    minFile += "\n"
    return minFile


def refreshDataClasses():
    tempMin = saveDataClassFolderToMinFile("Data\DataClasses")
    generateDataClassFiles("dataClasses.dataClass")
    tempMinList = tempMin.split("\n")
    try:
        tempMinList.remove("\n")
    except ValueError:
        pass
    lines = set(tempMinList)
    with open('Data/DataClasses/dataClasses.dataClass') as oldMin:
        t = oldMin.read().split("\n")
        try:
            t.remove("\n")
        except ValueError:
            pass
        lines |= set(t)
        new_lines = {}
    for line in lines:
        lineKey = line.split(",")[0]
        try:
            cur_line = new_lines[lineKey]
        except KeyError:
            cur_line = ""
        if len(line) > len(cur_line):
            new_lines[lineKey] = line
    result = new_lines.values()
    result.sort()
    try:
        result.remove("")
    except ValueError:
        pass
    with open('Data/DataClasses/dataClasses.dataClass', 'r+') as oldMin:
        oldMin.writelines("\n".join(result) + "\n")
        oldMin.truncate()

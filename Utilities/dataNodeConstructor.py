from dataNode import DataNode
import dataTypeConstructor
import json
import csv
from os import walk, path


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
            new_json["dataClass"] = value[2]
            new_json["parsedData"] = value[3]
            for key in new_json:
                if new_json[key] == "":
                    new_json[key] = None
            new_file = open(fileName, 'w')
            new_file.write(json.dumps(new_json, indent=4))
            new_file.close()
    return json.dumps(new_json, indent=4)


def generateDataNodeMinFile(inputJSON, fileLocation):
    rv = []
    j = json.loads(inputJSON)
    rv.append(fileLocation)
    rv.append(j["dataType"])
    rv.append(j["dataClass"])
    rv.append(j["parsedData"])

    rString = ""
    for i in rv:
        if type(i) is unicode or type(i) is str:
            rString += "\"" + i + "\""
        elif not i:
            pass
        else:
            rString += str(i)
        rString += ","

    if len(rString) > 0:
        rString = rString[:-1]
    return rString


def saveDataNodeFolderToMinFile(folderName):
    minFile = ""
    for subdir, dirs, files in walk(folderName):
        for file in files:
            file = path.join(subdir, file)
            file = file.replace("\\","/")
            if (file.endswith("json")):
                with open(file, 'r') as f:
                    minFile += generateDataNodeMinFile(f.read(), file)
                    minFile += "\n"
    return minFile


def refreshDataNodes():
    tempMin = saveDataNodeFolderToMinFile("Data\DataNodes")
    generateDataNodeFiles("dataNodes.dataNode")
    tempMinList = tempMin.split("\n")
    try:
        tempMinList.remove("\n")
    except ValueError:
        pass
    lines = set(tempMinList)
    with open('Data/DataNodes/dataNodes.dataNode') as oldMin:
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
    with open('Data/DataNodes/dataNodes.dataNode', 'r+') as oldMin:
        oldMin.writelines("\n".join(result) + "\n")
        oldMin.truncate()

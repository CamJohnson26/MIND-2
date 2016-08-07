from dataType import DataType
import Data.matchFunctions as matchFunctions
import csv
import json
from os import walk, path


def dataTypeFromJSON(inputJSON):
    inputObject = json.loads(inputJSON)
    dataTypeName = inputObject["dataTypeName"]
    matchFunction = getattr(matchFunctions, inputObject["matchFunction"])
    dataType = DataType(dataTypeName, matchFunction)
    return dataType


def loadDataType(inputFileName):
    f = open("Data/DataTypes/" + inputFileName)
    json = f.read()
    return dataTypeFromJSON(json)


def generateDataTypeFiles(minFileName):
    new_json = {"class": "DataType"}
    with open("Data/DataTypes/" + minFileName) as minFile:
        inputValues = csv.reader(minFile, delimiter=",", quotechar="\"")
        for value in inputValues:
            fileName = value[0]
            new_json["dataTypeName"] = value[1]
            new_json["matchFunction"] = value[2]
            for key in new_json:
                if new_json[key] == "":
                    new_json[key] = None
            new_file = open(fileName, 'w')
            new_file.write(json.dumps(new_json, indent=4))
            new_file.close()
    return json.dumps(new_json, indent=4)


def generateDataTypeMinFile(inputJSON, fileLocation):
    rv = []
    j = json.loads(inputJSON)
    rv.append(fileLocation)
    rv.append(j["dataTypeName"])
    rv.append(j["matchFunction"])

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


def saveDataTypeFolderToMinFile(folderName):
    minFile = ""
    for subdir, dirs, files in walk(folderName):
        for file in files:
            file = path.join(subdir, file)
            file = file.replace("\\","/")
            if (file.endswith("json")):
                with open(file, 'r') as f:
                    minFile += generateDataTypeMinFile(f.read(), file)
                    minFile += "\n"
    return minFile


def refreshDataTypes():
    tempMin = saveDataTypeFolderToMinFile("Data\DataTypes")
    generateDataTypeFiles("dataTypes.dataType")
    tempMinList = tempMin.split("\n")
    try:
        tempMinList.remove("\n")
    except ValueError:
        pass
    lines = set(tempMinList)
    with open('Data/DataTypes/dataTypes.dataType') as oldMin:
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
    with open('Data/DataTypes/dataTypes.dataType', 'r+') as oldMin:
        oldMin.writelines("\n".join(result) + "\n")
        oldMin.truncate()

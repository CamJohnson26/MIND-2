from dataType import DataType
import dataClassConstructor
import Data.matchFunctions as matchFunctions
import json


def dataTypeFromJSON(inputJSON):
    inputObject = json.loads(inputJSON)
    dataTypeName = inputObject["dataTypeName"]
    matchFunction = getattr(matchFunctions, inputObject["matchFunction"])
    dataType = DataType(dataTypeName, matchFunction)
    dataClasses = []
    for dataClass in inputObject["dataClasses"]:
        dataClasses.append(dataClassConstructor.dataClassFromJSON(json.dumps(dataClass)))
    dataType.dataClasses = dataClasses
    return dataType


def loadDataType(inputFileName):
    f = open("Data/DataTypes/" + inputFileName)
    json = f.read()
    return dataTypeFromJSON(json)

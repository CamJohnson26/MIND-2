from flowGraph import FlowGraph
from guidMapper import GuidMapper
import graphStructureConstructor
import json
import csv
from os import listdir, walk, path
from os.path import join


def flowGraphFromJSON(inputJSON, guidMapper=GuidMapper()):
    inputObject = json.loads(inputJSON)
    graph = graphStructureConstructor.graphStructureFromJSON(json.dumps(inputObject["graph"]), guidMapper=guidMapper)
    startNodes = []
    for node_id in inputObject["startNodes"]:
        for node in graph.nodes:
            if node.guid == guidMapper.get(node_id):
                startNodes.append(node)
    contextNodes = []
    for node_id in inputObject["contextNodes"]:
        for node in graph.nodes:
            if node.guid == guidMapper.get(node_id):
                contextNodes.append(node)
    flowGraph = FlowGraph(graph, startNodes, contextNodes=contextNodes)
    return flowGraph


def loadFlowGraph(inputFileName):
    f = open("Data/FlowGraphs/" + inputFileName)
    json = f.read()
    return flowGraphFromJSON(json)


def loadFlowGraphs(inputNames):
    rv = []
    for name in inputNames:
        rv.append(loadFlowGraph(name + ".json"))
    return rv


def generateFlowGraphFiles(minFileName):
    with open("Data/FlowGraphs/" + minFileName) as minFile:
        inputValues = csv.reader(minFile, delimiter=",", quotechar="\'")
        for value in inputValues:
            new_json = {"class": "FlowGraph"}
            new_json["graph"] = {"nodes": [], "guid": -1, "class": "GraphStructure"}
            fileName = value[0]
            nodes = json.loads(value[1])
            for n in nodes:
                new_node = {"class": "GraphNode", "dataClass": None}
                new_node["guid"] = int(n[0])
                new_node["dataNode"] = n[1]
                new_node["dataClass"] = n[2]
                new_node["nexts"] = n[3]
                new_json["graph"]["nodes"].append(new_node)
            new_json["startNodes"] = json.loads(value[2])
            new_json["contextNodes"] = json.loads(value[3])
            new_json["graph"]["name"] = value[4]
            for key in new_json:
                if new_json[key] == "":
                    new_json[key] = None
            new_file = open(fileName, 'w')
            new_file.write(json.dumps(new_json, indent=4))
            new_file.close()
    return json.dumps(new_json, indent=4)


def generateFlowGraphMinFile(inputJSON, fileLocation):
    rv = []
    j = json.loads(inputJSON)
    rv.append(fileLocation)

    newNodes = "["
    for i, n in enumerate(j["graph"]["nodes"]):
        newNodes += "["
        newNodes += str(i)
        newNodes += ","
        newNodes += "\"" + n["dataNode"] + "\"" if n["dataNode"] else "null"
        newNodes += ","
        newNodes += "\"" + n["dataClass"] + "\"" if n["dataClass"] else "null"
        newNodes += ","
        t = "["
        for k in n["nexts"]:
            if k:
                t += str(k)
            else:
                t += "null"
            t += ","
        if len(t) > 1:
            t = t[:-1]
        t += "]"
        newNodes += t
        newNodes += "]"
        newNodes += ","
    if len(newNodes) > 1:
        newNodes = newNodes[:-1]
    newNodes += "]"
    rv.append(newNodes)
    newNodes = "["
    for i, n in enumerate(j["startNodes"]):
        newNodes += str(i)
        newNodes += ","
    if len(newNodes) > 1:
        newNodes = newNodes[:-1]
    newNodes += "]"
    rv.append(newNodes)
    newNodes = "["
    for i, n in enumerate(j["contextNodes"]):
        newNodes += str(i)
        newNodes += ","
    if len(newNodes) > 1:
        newNodes = newNodes[:-1]
    newNodes += "]"
    rv.append(newNodes)
    rv.append(j["graph"]["name"])

    rString = ""
    for i in rv:
        if type(i) is unicode or type(i) is str:
            rString += "\'" + i + "\'"
        elif not i:
            pass
        else:
            rString += str(i)
        rString += ","

    if len(rString) > 0:
        rString = rString[:-1]
    return rString


def createMinFileForWord(word):
    minFile = "'words/" + word + ".json','["
    for i, c in enumerate(word):
        if i == len(word) - 1:
            n = "null"
        else:
            n = str(i + 1)
        node = '[' + str(i) + ',"letter.json","letters/class_' + c + '.json",[' + n + ']],'
        minFile += node
    minFile = minFile[:-1]
    minFile += "]','[0]','[]','class:" + word + "'\n"


    with open("Data/FlowGraphs/flowGraphs.flowGraph", "a") as f:
        f.write(minFile)

    index = 0
    with open("Data/DataClasses/dataClasses.dataClass") as f:
        inputValues = csv.reader(f, delimiter=",", quotechar="\'")
        for value in inputValues:
            index = int(value[1])

    minDataClass = '"words/' + word + '.json",' + str(index + 1) + ',"' + word + '","words/' + word + '.json"\n'

    with open("Data/DataClasses/dataClasses.dataClass", "a") as f:
        f.write(minDataClass)


def saveFlowGraphFolderToMinFile(folderName):
    minFile = ""
    for subdir, dirs, files in walk(folderName):
        for file in files:
            file = path.join(subdir, file)
            file = file.replace("\\","/")
            if (file.endswith("json")):
                with open(file, 'r') as f:
                    minFile += generateFlowGraphMinFile(f.read(), file)
                    minFile += "\n"
    return minFile


def refreshFlowGraphs():
    tempMin = saveFlowGraphFolderToMinFile("Data/FlowGraphs")
    generateFlowGraphFiles("flowGraphs.flowGraph")
    tempMinList = tempMin.split("\n")
    try:
        tempMinList.remove("\n")
    except ValueError:
        pass
    lines = set(tempMinList)
    with open('Data/FlowGraphs/flowGraphs.flowGraph') as oldMin:
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
    with open('Data/FlowGraphs/flowGraphs.flowGraph', 'r+') as oldMin:
        oldMin.writelines("\n".join(result) + "\n")
        oldMin.truncate()

from graphNode import GraphNode
import dataNodeConstructor
import json


def graphNodeFromJSON(inputJSON):
    inputObject = json.loads(inputJSON)
    if type(inputObject["dataNode"]) is unicode:
        dataNode = dataNodeConstructor.loadDataNode(inputObject["dataNode"])
    else:
        node_json = json.dumps(inputObject["dataNode"])
        dataNode = dataNodeConstructor.dataNodeFromJSON(node_json)
    graphNode = GraphNode(dataNode)
    graphNode.guid = inputObject["guid"]
    graphNode.nexts = []
    return graphNode

from graphNode import GraphNode
import dataNodeConstructor
import json


def graphNodeFromJSON(inputJSON):
    inputObject = json.loads(inputJSON)
    dataNode = dataNodeConstructor.dataNodeFromJSON(json.dumps(inputObject["dataNode"]))
    graphNode = GraphNode(dataNode)
    graphNode.guid = inputObject["guid"]
    graphNode.nexts = []
    return graphNode

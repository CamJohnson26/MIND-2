from graphStructure import GraphStructure
from Utilities.guidMapper import GuidMapper
import Utilities.graphNodeConstructor
import json


def graphStructureFromJSON(inputJSON, guidMapper=GuidMapper()):
    inputObject = json.loads(inputJSON)
    name = inputObject["name"]
    nodes = []
    nodeGuids = {}
    for node in inputObject["nodes"]:
        new_node = Utilities.graphNodeConstructor.graphNodeFromJSON(json.dumps(node), guidMapper=guidMapper)
        nodeGuids[new_node.guid] = new_node
        nodes.append(new_node)
    for node in inputObject["nodes"]:
        current_node = nodeGuids[guidMapper.get(node["guid"])]
        new_nexts = []
        for next_id in node["nexts"]:
            if next_id is None:
                new_nexts.append(None)
            else:
                new_nexts.append(nodeGuids[guidMapper.get(next_id)])
        current_node.nexts = new_nexts
    graphStructure = GraphStructure(nodes, name)
    graphStructure.guid = guidMapper.get(inputObject["guid"])
    return graphStructure

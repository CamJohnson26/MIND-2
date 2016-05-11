from graphStructure import GraphStructure
import graphNodeConstructor
import json


def graphStructureFromJSON(inputJSON):
    inputObject = json.loads(inputJSON)
    name = inputObject["name"]
    nodes = []
    nodeGuids = {}
    for node in inputObject["nodes"]:
        new_node = graphNodeConstructor.graphNodeFromJSON(json.dumps(node))
        nodeGuids[new_node.guid] = new_node
        nodes.append(new_node)
    for node in inputObject["nodes"]:
        current_node = nodeGuids[node["guid"]]
        new_nexts = []
        for next_id in node["nexts"]:
            if next_id is None:
                new_nexts.append(None)
            else:
                new_nexts.append(nodeGuids[next_id])
        current_node.nexts = new_nexts
    graphStructure = GraphStructure(nodes, name)
    graphStructure.guid = inputObject["guid"]
    return graphStructure

from dataGraph import DataGraph
import graphStructureConstructor
import json


def flowGraphFromJSON(inputJSON):
    inputObject = json.loads(inputJSON)
    graph = graphStructureConstructor.graphStructureFromJSON(json.dumps(inputObject["graph"]))
    dataGraph = DataGraph(graph)
    return dataGraph

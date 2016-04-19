import json


class DataGraphFlattener:

    dataGraph = None

    def __init__(self, dataGraph):
        self.dataGraph = dataGraph

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "DataGraphFlattener"}
        return rv

    def flat_graph(self):
        rv = []
        currentNode = self.dataGraph.graph.nodes[0]
        while currentNode is not None:
            rv.append(currentNode)
            currentNode = self.compare_nodes(currentNode.nexts)
        return rv

    def compare_nodes(self, nodes):
        return nodes[0]

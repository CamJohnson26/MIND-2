import json


class ChainGraphFlattener:

    chainGraph = None

    def __init__(self, chainGraph):
        self.chainGraph = chainGraph

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "ChainGraphFlattener"}
        return rv

    def flat_graph(self):
        rv = []
        currentNode = self.chainGraph.graph.nodes[0]
        while currentNode is not None:
            rv.append(currentNode)
            currentNode = self.compare_nodes(currentNode.nexts)
        return rv

    def compare_nodes(self, nodes):
        return nodes[0]

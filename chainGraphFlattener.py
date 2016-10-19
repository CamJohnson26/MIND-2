import json


class ChainGraphFlattener:

    chainGraph = None

    def __init__(self, chainGraph):
        self.chainGraph = chainGraph

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def __repr__(self):
        return json.dumps(self.get_json())

    def get_json(self):
        """
        Get JSON representation of class

        :return: str
        """
        rv = {"class": "ChainGraphFlattener"}
        return rv

    def flat_graph(self):
        """
        Remove all branches from a chainGraph

        :return: str
        """
        rv = []
        currentNode = self.chainGraph.graph.nodes[0]
        while currentNode is not None:
            rv.append(currentNode)
            currentNode = self.compare_nodes(currentNode.nexts)
        return rv

    def compare_nodes(self, nodes):
        """
        Given a list of nodes, choose one

        :param nodes: list of nodes to compare
        :return: graphNode
        """
        return nodes[0]


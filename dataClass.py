import json
from graphNode import GraphNode
from chainGraph import ChainGraph
from graphStructure import GraphStructure


class DataClass:
    """
    One of a discrete set of allowed classes for some object
    """

    flowGraph = None
    dataClassIndex = 0
    dataClassString = ""
    dataClasses = {}

    def __init__(self, flowGraph, dataClassIndex, dataClassString):
        self.flowGraph = flowGraph
        self.dataClassIndex = dataClassIndex
        self.dataClassString = dataClassString
        self.dataClasses = {}

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def __repr__(self):
        return json.dumps(self.get_json())

    def get_json(self):
        """
        Get JSON representation of class

        :return: str
        """
        rv = {"class": "DataClass"}
        if self.flowGraph:
            rv["flowGraph"] = self.flowGraph.get_json()
        else:
            rv["flowGraph"] = None
        rv["dataClassIndex"] = self.dataClassIndex
        rv["dataClassString"] = self.dataClassString
        dataClassesJson = {}
        for key in self.dataClasses.keys():
            if self.dataClasses[key]:
                if type(self.dataClasses[key]) in [str]:
                    dataClassesJson[key] = self.dataClasses[key]
                else:
                    dataClassesJson[key] = self.dataClasses[key].get_json()
            else:
                dataClassesJson[key] = None
        rv["dataClasses"] = dataClassesJson
        return rv

    def matches(self, dataNode):
        """
        Does the given dataNode match this class?

        :param dataNode:
        :return: boolean
        """
        if type(dataNode.parsedData) in [str]:
            nodes = [GraphNode(dataNode)]
            graphStructure = GraphStructure(nodes, self.dataClassString)
            chainGraph = ChainGraph(graphStructure)
        else:
            chainGraph = dataNode.parsedData
        return self.flowGraph.matches_chainGraph(chainGraph)

    def rollup_classes(self):
        """
        Since dataClasses can have dataClasses, make sure all children are accessible to the parent

        :return: None
        """
        for key in self.dataClasses.keys():
            if self.dataClasses[key]:
                self.dataClasses[key].rollup_classes()
        temp_dataClasses = {}
        for key in self.dataClasses.keys():
            if self.dataClasses[key]:
                for k in self.dataClasses[key].dataClasses.keys():
                    temp_dataClasses[k] = self.dataClasses[key].dataClasses[k]
        for key in temp_dataClasses.keys():
            self.dataClasses[key] = temp_dataClasses[key]

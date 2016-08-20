import uuid
import json


class GraphNode:

    dataNode = None
    dataClasses = {}
    nexts = []
    guid = ""

    def __init__(self, dataNode):
        self.dataNode = dataNode
        self.dataClasses = {"dataIndex": None}
        self.guid = uuid.uuid4()
        self.nexts = []

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_copy(self):
        copy = GraphNode(self.dataNode)
        for key in self.dataClasses:
            copy.dataClasses[key] = self.dataClasses[key]
        copy.nexts = [n for n in self.nexts]
        return copy

    def get_json(self):
        rv = {"class": "GraphNode"}
        rv["dataNode"] = self.dataNode.get_json()
        rv["guid"] = str(self.guid)
        rv["nexts"] = [str(a.guid) for a in self.nexts if a is not None]
        rv["nexts"].extend([a for a in self.nexts if a is None])
        dataClassesJson = {}
        for key in self.dataClasses.keys():
            if self.dataClasses[key]:
                dataClassesJson[key] = self.dataClasses[key].get_json()
            else:
                dataClassesJson[key] = None
        rv["dataClasses"] = dataClassesJson
        return rv

    def matches(self, inputData):
        inputDataTypeName = inputData.dataNode.dataType.dataTypeName
        inputDataParsedData = inputData.dataNode.parsedData
        dataClassMatches = True
        for dataClassKey in self.dataClasses.keys():
            inputDataClass = inputData.dataClasses.get(dataClassKey)
            inputDataClassIndex = None
            if inputDataClass:
                inputDataClassIndex = inputDataClass.dataClassIndex
            dataClass = self.dataClasses[dataClassKey]
            if not (dataClass is None or                                          # Data Classes are equal
             (dataClass.dataClassIndex == inputDataClassIndex)):
                dataClassMatches = False
        if (((self.dataNode.dataType.dataTypeName == inputDataTypeName) and     # Data Types are equal
            dataClassMatches and        # Data Classes are equal
            ((self.dataNode.parsedData == inputDataParsedData) or               # Parsed Data is equal or null
            (self.dataNode.parsedData is None))) or                             # OR
            ((self.dataNode.parsedData is None) and                             # Parsed data is null and
             self.dataNode.dataType.matches(inputDataParsedData)) and           # Matches Function works and
            dataClassMatches):
            return True
        else:
            return False

    def get_matching_classes(self, dataClasses):
        if self.dataNode.dataType.dataTypeName == "word":
            pass
        matches = []
        try:
            for c in dataClasses[self.dataNode.dataType.dataTypeName]:
                if c.matches(self.dataNode):
                    matches.append(c)
        except KeyError:
            pass
        return matches

    def rollup_dataClass(self, dataClass):
        dataClass.rollup_classes()
        for key in dataClass.dataClasses.keys():
            self.dataClasses[key] = dataClass.dataClasses[key]

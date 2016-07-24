import uuid
import json


class GraphNode:

    dataNode = None
    dataClass = None
    nexts = []
    guid = ""

    def __init__(self, dataNode):
        self.dataNode = dataNode
        self.dataClass = None
        self.guid = uuid.uuid4()
        self.nexts = []

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "GraphNode"}
        rv["dataNode"] = self.dataNode.get_json()
        rv["guid"] = str(self.guid)
        rv["nexts"] = [str(a.guid) for a in self.nexts if a is not None]
        rv["nexts"].extend([a for a in self.nexts if a is None])
        if self.dataClass:
            rv["dataClass"] = self.dataClass.get_json()
        else:
            rv["dataClass"] = None
        return rv

    def matches(self, inputData):
        inputDataTypeName = inputData.dataNode.dataType.dataTypeName
        inputDataClass = inputData.dataClass
        inputDataClassIndex = None
        if inputDataClass:
            inputDataClassIndex = inputDataClass.dataClassIndex
        inputDataParsedData = inputData.dataNode.parsedData
        if (((self.dataNode.dataType.dataTypeName == inputDataTypeName) and     # Data Types are equal
            (self.dataClass is None or
             (self.dataClass.dataClassIndex == inputDataClassIndex)) and        # Data Classes are equal
            ((self.dataNode.parsedData == inputDataParsedData) or               # Parsed Data is equal or null
            (self.dataNode.parsedData is None))) or                             # OR
            ((self.dataNode.parsedData is None) and                             # Parsed data is null and
             self.dataNode.dataType.matches(inputDataParsedData)) and           # Matches Function works and
            (self.dataClass is None or                                          # Data Classes are equal
             (self.dataClass.dataClassIndex == inputDataClassIndex))):
            return True
        else:
            return False

    def classify(self, dataClasses):
        dataClass = None
        try:
            for c in dataClasses[self.dataNode.dataType.dataTypeName]:
                if c.matches(self.dataNode):
                    dataClass = c
        except KeyError:
            pass
        self.dataClass = dataClass

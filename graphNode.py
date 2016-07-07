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
        if (((self.dataNode.dataType.dataTypeName == inputDataTypeName) and
            (self.dataClass is None or
             self.dataClass.dataClassIndex == inputDataClassIndex) and
            ((self.dataNode.parsedData == inputDataParsedData) or
            (self.dataNode.parsedData is None))) or
            ((self.dataNode.parsedData is None) and
             self.dataNode.dataType.matches(inputData.dataNode.parsedData))):
            return True
        else:
            return False

    def classify(self, dataClasses):
        dataClass = None
        for c in dataClasses:
            if c.matches(self.dataNode):
                dataClass = c
        self.dataClass = dataClass

import uuid
import json


class GraphNode:

    dataNode = None
    nexts = []
    guid = ""

    def __init__(self, dataNode):
        self.dataNode = dataNode
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
        return rv

    def matches(self, inputData):
        if (self.dataNode.matches(inputData.dataNode.parsedData) or
           (self.dataNode.dataType == inputData.dataNode.dataType)):
            return True
        else:
            return False

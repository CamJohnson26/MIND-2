import uuid
import json


class BridgeNode:

    startGraphNode = None
    endGraphNode = None
    targetGraphNode = None
    guid = ""

    def __init__(self):
        self.startGraphNode = None
        self.endGraphNode = None
        self.targetGraphNode = None
        self.guid = uuid.uuid4()

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "ParseNode"}
        rv["startGraphNode"] = self.startGraphNode.get_json()
        rv["endGraphNode"] = self.endGraphNode.get_json()
        rv["targetGraphNode"] = self.targetGraphNode.get_json()
        rv["guid"] = str(self.guid)
        return rv
    # Merge this class with Cursor, or create a new DataGraph cursor

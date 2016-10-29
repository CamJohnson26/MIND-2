import uuid
import json


class BridgeNode:
    """
    Links 2 chain graphs together with a start, an end, and a target

    """
    startGraphNode = None
    endGraphNode = None
    targetGraphNode = None
    guid = ""

    def __init__(self,
                 startGraphNode=None,
                 endGraphNode=None,
                 targetGraphNode=None):
        self.startGraphNode = startGraphNode
        self.endGraphNode = endGraphNode
        self.targetGraphNode = targetGraphNode
        self.guid = uuid.uuid4()

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def __repr__(self):
        return json.dumps(self.get_json())

    def get_json(self):
        """
        Get JSON representation of class

        :return: str
        """
        rv = {"class": "ParseNode"}
        rv["startGraphNode"] = self.startGraphNode.get_json()
        rv["endGraphNode"] = self.endGraphNode.get_json()
        rv["targetGraphNode"] = self.targetGraphNode.get_json()
        rv["guid"] = str(self.guid)
        return rv

    def get_copy(self):
        """
        Create a copy of this object

        :return: BridgeNode
        """
        copy = BridgeNode(startGraphNode=self.startGraphNode,
                          endGraphNode=self.endGraphNode,
                          targetGraphNode=self.targetGraphNode)
        return copy

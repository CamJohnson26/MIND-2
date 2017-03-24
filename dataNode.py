import json


class DataNode:
    """
    A specific piece of information that can be inserted in a graphNode and has a dataType
    """
    dataType = None
    parsedData = ""

    def __init__(self, dataType, parsedData=None):
        self.dataType = dataType
        self.parsedData = parsedData

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def __repr__(self):
        return json.dumps(self.get_json())

    def get_json(self):
        """
        Get JSON representation of class

        :return: str
        """
        rv = {"class": "DataNode"}
        rv["dataType"] = self.dataType.get_json()
        if not self.parsedData:
            rv["parsedData"] = None
        elif type(self.parsedData) in [str]:
            rv["parsedData"] = self.parsedData
        else:
            rv["parsedData"] = self.parsedData.get_json()
        return rv

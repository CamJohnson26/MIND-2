import json


class DataNode:

    dataType = None
    parsedData = ""

    def __init__(self, dataType, parsedData=""):
        self.dataType = dataType
        self.parsedData = parsedData

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "DataNode"}
        rv["dataType"] = self.dataType.get_json()
        if type(self.parsedData) is str:
            rv["parsedData"] = self.parsedData
        else:
            rv["parsedData"] = self.parsedData.get_json()
        return rv

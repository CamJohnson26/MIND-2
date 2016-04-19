import json


class DataNode:

    matchFunction = None
    dataType = ""
    parsedData = ""

    def __init__(self, dataType, matchFunction, parsedData=""):
        self.dataType = dataType
        self.matchFunction = matchFunction
        self.parsedData = parsedData

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "DataNode"}
        rv["dataType"] = self.dataType
        if type(self.parsedData) is str:
            rv["parsedData"] = self.parsedData
        else:
            rv["parsedData"] = self.parsedData.get_json()
        return rv

    def matches(self, inputVal):
        return self.matchFunction(inputVal)

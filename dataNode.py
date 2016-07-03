import json


class DataNode:

    dataType = None
    dataClass = None
    parsedData = ""

    def __init__(self, dataType, parsedData=None):
        self.dataType = dataType
        self.parsedData = parsedData
        self.dataClass = None

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "DataNode"}
        rv["dataType"] = self.dataType.get_json()
        if not self.parsedData:
            rv["parsedData"] = None
        elif type(self.parsedData) in [str, unicode]:
            rv["parsedData"] = self.parsedData
        else:
            rv["parsedData"] = self.parsedData.get_json()
        if self.dataClass:
            rv["dataClass"] = self.dataClass.get_json()
        else:
            rv["dataClass"] = None
        return rv

    def classify(self, dataClasses):
        dataClass = None
        for c in dataClasses:
            if c.matches(self):
                dataClass = c
        self.dataClass = dataClass

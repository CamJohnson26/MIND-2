import json


class DataType:

    matchFunction = None
    dataTypeName = ""
    dataClasses = []

    def __init__(self, dataTypeName, matchFunction):
        self.dataTypeName = dataTypeName
        self.matchFunction = matchFunction
        self.dataClasses = []

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "DataType"}
        rv["dataTypeName"] = self.dataTypeName
        rv["dataClasses"] = [a.get_json() for a in self.dataClasses]
        rv["matchFunction"] = self.matchFunction.__name__
        return rv

    def matches(self, inputVal):
        return self.matchFunction(inputVal)

    def classify(self, dataNode):
        for c in self.dataClasses:
            if c.matches(dataNode):
                return c

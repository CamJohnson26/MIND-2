import json


class DataType:

    matchFunction = None
    dataTypeName = ""
    dataClassName = ""

    def __init__(self, dataTypeName, dataClassName, matchFunction):
        self.dataTypeName = dataTypeName
        self.dataClassName = dataClassName
        self.matchFunction = matchFunction

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "DataType"}
        rv["dataTypeName"] = self.dataTypeName
        rv["dataClassName"] = self.dataClassName
        rv["matchFunction"] = self.matchFunction.__name__
        return rv

    def matches(self, inputVal):
        return self.matchFunction(inputVal)

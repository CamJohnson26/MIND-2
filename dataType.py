import json


class DataType:

    matchFunction = None
    dataTypeName = ""
    dataClasses = {}

    def __init__(self, dataTypeName, dataClasses, matchFunction):
        self.dataTypeName = dataTypeName
        self.dataClasses = dataClasses
        self.matchFunction = matchFunction

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "DataType"}
        rv["dataTypeName"] = self.dataTypeName
        rv["dataClasses"] = json.dumps(self.dataClasses)
        rv["matchFunction"] = self.matchFunction.__name__
        return rv

    def matches(self, inputVal):
        return self.matchFunction(inputVal)

import json


class DataType:

    matchFunction = None
    dataTypeName = ""
    dataClasses = {}

    def __init__(self, dataTypeName, dataClasses, matchFunction):
        self.dataTypeName = dataTypeName
        self.dataClasses = {}
        for key in dataClasses.keys():
            self.dataClasses[key] = dataClasses[key]
        self.matchFunction = matchFunction

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def get_json(self):
        rv = {"class": "DataType"}
        rv["dataTypeName"] = self.dataTypeName
        dataClassesJson = {}
        for key in self.dataClasses.keys():
            if self.dataClasses[key]:
                dataClassesJson[key] = self.dataClasses[key]
            else:
                dataClassesJson[key] = None
        rv["dataClasses"] = dataClassesJson
        rv["matchFunction"] = self.matchFunction.__name__
        return rv

    def matches(self, inputVal):
        return self.matchFunction(inputVal)

import json


class DataType:
    """
    A named piece of information that matches some function and can have classes
    """

    matchFunction = None
    dataTypeName = ""
    dataClasses = {}

    def __init__(self, dataTypeName, dataClasses, matchFunction):
        self.dataTypeName = dataTypeName
        self.dataClasses = {}
        for key in dataClasses.keys():
            self.dataClasses[key] = dataClasses[key]
            #for data_class_key in dataClasses[key]:
            #    self.dataClasses[key][data_class_key] = dataClasses[key][data_class_key]
        self.matchFunction = matchFunction

    def __str__(self):
        return json.dumps(self.get_json(), indent=4)

    def __repr__(self):
        return json.dumps(self.get_json())

    def get_json(self):
        """
        Get JSON representation of class

        :return: str
        """
        rv = {"class": "DataType"}
        rv["dataTypeName"] = self.dataTypeName
        dataClassesJson = {}
        for key in self.dataClasses.keys():
            if self.dataClasses[key]:
                dataClassesJson[key] = {}
                for data_class_key in self.dataClasses[key]:
                    dataClassesJson[key][data_class_key] = self.dataClasses[key][data_class_key].get_json()
            else:
                dataClassesJson[key] = None
        rv["dataClasses"] = dataClassesJson
        rv["matchFunction"] = self.matchFunction.__name__
        return rv

    def matches(self, inputVal):
        """

        :param inputVal:
        :return: boolean
        """
        return self.matchFunction(inputVal)

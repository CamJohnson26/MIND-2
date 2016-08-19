from os import listdir, walk, path
from os.path import isfile, join
from abc import ABCMeta, abstractmethod
import csv


class AbstractFileManager():

    __metaclass__ = ABCMeta

    home_folder = ""
    min_file_name = ""

    def __init__(self, home_folder, min_file_name):
        self.home_folder = home_folder
        self.min_file_name = min_file_name

    @abstractmethod
    def objectFromJSON(self, inputJSON):
        return NotImplementedError

    @abstractmethod
    def min_file_to_json(self, minFile):
        return NotImplementedError

    @abstractmethod
    def json_to_min_file(self, inputJSON, fileLocation):
        return NotImplementedError

    def loadObject(self, inputFileName):
        f = open(join(self.home_folder, inputFileName))
        json = f.read()
        return self.objectFromJSON(json)

    def loadObjects(self, inputFolder):
        rv = []
        if type(inputFolder) is list:
            files = [str(f) + ".json" for f in inputFolder]
        else:
            path = join(self.home_folder, inputFolder)
            files = listdir(path)
            files = [join(inputFolder, f) for f in files if isfile(join(path, f))]
        for file in files:
            f = open(join(self.home_folder, file))
            json = f.read()
            rv.append(self.objectFromJSON(json))
        return rv

    def generateFiles(self):
        with open(join(self.home_folder, self.min_file_name)) as minFile:
            lines = minFile.readlines()
            for line in lines:
                new_json = self.min_file_to_json(line)
                fileName = self.min_file_to_array(line)[0]
                new_file = open(fileName, 'w')
                new_file.write(new_json)
                new_file.close()

    def refreshObjects(self):
        tempMin = self.save_folder_to_min_file(self.home_folder)
        self.dedup_min_file(tempMin)
        self.generateFiles()

    def add_minObject_to_file(minObject):
        with open(join(self.home_folder, self.min_file_name), 'a') as minFile:
            minFile.write(minObject + "\n")

    @staticmethod
    def min_file_to_array(minFile):
        return list(csv.reader([minFile], delimiter=",", quotechar="'"))[0]

    @staticmethod
    def array_to_min(iarray):
        rString = ""
        for i in iarray:
            if type(i) is unicode or type(i) is str:
                rString += "\'" + i + "\'"
            elif type(i) is list:
                rString += ("[" + ",".join([dc for dc in i]) + "]")
            elif type(i) is dict:
                rString += "'{"
                for key in i.keys():
                    rString += "\"" + key + "\":\"" + i[key] + "\","
                if len(i.keys()) > 0:
                    rString = rString[:-1]
                rString += "}'"
            elif type(i) is int:
                rString += str(i)
            elif not i:
                pass
            else:
                rString += str(i)
            rString += ","

        if len(rString) > 0:
            rString = rString[:-1]
        return rString

    def save_folder_to_min_file(self, folder):
        minFile = ""
        for subdir, dirs, files in walk(join(self.home_folder, folder)):
            for file in files:
                file = path.join(subdir, file)
                file = file.replace("\\", "/")
                if (file.endswith("json")):
                    with open(file, 'r') as f:
                        minFile += self.json_to_min_file(f.read(), file)
                        minFile += "\n"
        return minFile

    def dedup_min_file(self, tempMin):
        fileLocation = join(self.home_folder, self.min_file_name)
        tempMinList = tempMin.split("\n")
        try:
            tempMinList.remove("\n")
        except ValueError:
            pass
        lines = set(tempMinList)
        with open(fileLocation) as oldMin:
            t = oldMin.read().split("\n")
            try:
                t.remove("\n")
            except ValueError:
                pass
            lines |= set(t)
        new_lines = {}
        for line in lines:
            lineKey = line.split(",")[0]
            try:
                cur_line = new_lines[lineKey]
            except KeyError:
                cur_line = ""
            if len(line) > len(cur_line):
                new_lines[lineKey] = line
        result = new_lines.values()
        result.sort()
        try:
            result.remove("")
        except ValueError:
            pass
        with open(fileLocation, 'r+') as oldMin:
            oldMin.writelines("\n".join(result) + "\n")
            oldMin.truncate()

from Utilities.constructors import *
from fileManagement import *

# path = words/dataIndex
# flowGraph = JSON
# name = ability
# dataClasses = JSON
def create_dataClassElement(path, dataClass, name, dataClasses):
    index = get_index_for_minFile("Data/DataClasses/dataClasses.dataClass")
    jsonRep = {"dataClassIndex": index, "dataClasses": dataClasses, "dataClassString": name, "class": "DataClass", "flowGraph": path + "/" + name + ".json"}
    minFile = generateDataClassMinFile(json.dumps(jsonRep), "Data/DataClasses/" + path + "/" + dataClass + "/" + name + ".json")
    add_minObject_to_file(minFile, "Data/DataClasses/dataClasses.dataClass")



def create_word(word, dataClasses):
    minFile = "'Data/FlowGraphs/words/" + word + ".json','["
    for i, c in enumerate(word):
        if i == len(word) - 1:
            n = "null"
        else:
            n = str(i + 1)
        node = '[' + str(i) + ',"letter.json",{"dataIndex":"letters/dataIndex/class_' + c + '.json"},[' + n + ']],'
        minFile += node
    minFile = minFile[:-1]
    minFile += "]','[0]','[]','class:" + word + "'\n"
    add_minObject_to_file(minFile, "Data/FlowGraphs/flowGraphs.flowGraph")

    create_dataClassElement("words", "dataIndex", word, dataClasses)


def create_word_attribute(word, attribute):
    create_word(word)

    minFile = "'Data/FlowGraphs/words/" + attribute + "s/" + word + ".json','[[0,\"word.json\",{\"dataIndex\":\"words/" + word + ".json\"},[null]]]','[0]','[]','" + attribute + ":" + word + "'\n"

    with open("Data/FlowGraphs/flowGraphs.flowGraph", "a") as f:
        f.write(minFile)

    index = 0
    with open("Data/DataClasses/dataClasses.dataClass") as f:
        inputValues = csv.reader(f, delimiter=",", quotechar="\'")
        for value in inputValues:
            if int(value[1]) > index:
                    index = int(value[1])

    index += 1

    minDataClass = '"Data/DataClasses/words/' + attribute + 's/' + word + '.json",' + str(index) + ',"' + word + '","words/' + attribute + 's/' + word + '.json"\n'
    with open("Data/DataClasses/dataClasses.dataClass", "a") as f:
        f.write(minDataClass)

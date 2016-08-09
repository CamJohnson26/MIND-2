from Utilities.constructors import *
import json
import os

# for w in ['all', 'month', 'four', 'facilities', 'bomber', 'to', 'not', 'friendly', 'relocated', 'nos', 'risk', 'returning', 'every', 'airfieldno', 'hour', 'having', 'mm', 'accommodationthe', 'force', 'second', 'pass', 'commander', 'targets',  'korea', 'above', 'new', 'ground', 'harassing', 'collateral', 'led', 'tengah', 'ranged', 'hours', 'green', 'supplying', 'commonwealth', 'search', 'shift', 'smoke', 'defeat', 'military', 'group', 'campaign', 'danger', 'airlifting', 'richmond', 'aur', 'unit', 'malaya', 'europe', 'australia', 'from', 'troops', 'would', 'joint', 'turret', 'june', 'flights', 'by', 'achieving', 'squadrons', 'rnzaf', 'ministry', 'propellers', 'sortie', 'casualties', 'appointed', 'fly', 'augment', 'this', 'work',  'following', 'drops', 'heffernan', 'impracticality', 'borneo', 'parachute', 'requirements', 'imminent', 'six', 'damage', 'formations', 'machine', 'located', 'crashlanding', 'undertook', 'badly', 'replacing', 'after', 'british', 'a', 'bombers', 'attempt', 'headquarters', 'one', 'maintain', 'so', 'jungle', 'began', 'operations', 'failureno', 'soof', 'insurgency', 'over', 'mainly', 'mission', 'held', 'including', 'its', 'bombing', 'raf', 'police', 'no', 'crew', 'strafe', 'them', 'civilian', 'troopsfourengined', 'flew', 'touching', 'they', 'half', 'arriving', 'day', 'drop', 'airlifting', 'found', 'transport', 'heavy', 'reduce', 'owing', 'firepower', 'out', 'contend', 'driving', 'kampong', 'base', 'could', 'turn', 'conducted', 'place', 'semipermanent', 'speeds', 'first', 'major', 'there', 'one', 'spinning', 'another', 'centre', 'their', 'messing', 'participated', 'wings', 'overshooting', 'lincoln', 'courier', 'that', 'completed', 'took', 'part', 'vips', 'target', 'transferred', 'were',  'sustaining', 'have', 'strength', 'after', 'able', 'also', 'take', 'forces', 'towards', 'cargo', 'eight', 'strikes', 'commanding',  'approved', 'considered', 'later', 'bomb', 'parked', 'range', 'staff', 'slow', 'redmond', 'behind', 'only', 'bases', 'communist', 'do', 'cannon', 'areas', 'guns', 'withdrawal', 'insurgents', 'where', 'concert', 'result', 'operated', 'despatch', 'staffed', 'written', 'cooperation', 'routine',  'ability', 'complement', 'aircraft', 'key', 'squadron', 'missions', 'many', 'against', 'load', 'supply', 'authorised', 'acted', 'throughout', 'war', 'iwakuni', 'strategy', 'reduction', 'dropping', 'maintenance', 'engine', 'pathfinders', 'partly', 'fire', 'ensuring', 'kuala', 'overrunning', 'suspected', 'rafs', 'pilot', 'landing', 'runway', 'air', 'lincolns', 'bomber', 'it', 'brake',  'damaged', 'make', 'same', 'injured', 'upon', 'flown', 'purpose', 'off', 'well', 'command',   'responsible', 'departed', 'generally', 'rotated', 'kill', 'previous', 'canisters', 'had',  'although',  'increased', 'possible', 'air',  'rear', 'lost', 'officer', 'night', 'dakota', 'security', 'antiaircraft', 'back', 'dakotas', 'duration', 'headlam', 'provided', 'dense', 'pinpoint', 'for', 'frank', 'be', 'run', 'power', 'command', 'offset', 'pahang', 'operation',  'central', 'december', 'completing', 'copiloted', 'japan', 'captain', 'slightly', 'or', 'own', 'presence', 'into', 'down', 'lumpur', 'strip', 'korean', 'communists', 'area', 'composite', 'support', 'initial', 'low', 'resulted', 'november',  'but', 'failure', 'tasked', 'with', 'he', 'up', 'they', 'propaganda', 'sometimes', 'aerial', 'singly', 'an', 'to', 'as',  'trailing', 'personnel', 'when', 'other', 'philippines', 'requested', 'february', 'hideouts', 'april', 'suited', 'leaflets', 'missionsthe', 'demoralising', 'original']:
#   createMinFileForWord(w)

# generateDataTypeFiles("dataTypes.dataType")
# generateDataNodeFiles("dataNodes.dataNode")
#generateDataClassFiles("Data\DataClasses\dataClasses.dataClass")
# generateFlowGraphFiles("flowGraphs.flowGraph")

#print(saveDataClassFolderToMinFile("Data\DataClasses"))
# print(saveDataTypeFolderToMinFile("Data\DataTypes"))
# print(saveFlowGraphFolderToMinFile("Data\FlowGraphs"))
# print(saveDataNodeFolderToMinFile("Data\DataNodes"))


def refreshData():
    refreshDataTypes()
    refreshDataNodes()
    refreshDataClasses()
    refreshFlowGraphs()

    updateWordAttribute("adjective")
    updateWordAttribute("adverb")
    updateWordAttribute("article")
    updateWordAttribute("conjunction")
    updateWordAttribute("noun")
    updateWordAttribute("preposition")
    updateWordAttribute("properNoun")
    updateWordAttribute("verb")

    refreshDataClasses()
    refreshFlowGraphs()


def clean_json():
    folder = "Data"
    to_delete = []
    for dirName, subdirList, fileList in os.walk(folder):
        for file in fileList:
            if file.endswith(".json"):
                to_delete.append(os.path.join(dirName, file))
    for f in to_delete:
        os.remove(f)
        print("Deleted file: " + f)
    print("Deleted " + str(len(to_delete)) + " files")


def updateWordAttribute(attribute):
    path = "Data/FlowGraphs/words/" + attribute + "s/"
    files = listdir(path)
    files = [f for f in files if isfile(join(path, f)) and f != (attribute + '.json')]

    file_json = {"graph": {"nodes": [], "guid": -1, "class": "GraphStructure", "name": attribute}, "contextNodes": [], "class": "FlowGraph", "startNodes": [] }
    for index, file in enumerate(files):
        node = {"dataClass": "words/" + file, "guid": index, "dataNode": "word.json", "class": "GraphNode", "nexts": [None] }
        file_json["graph"]["nodes"].append(node)
        file_json["startNodes"].append(index)

    with open("Data/FlowGraphs/flowGraphs.flowGraph", "a") as f:
        minFile = generateFlowGraphMinFile(json.dumps(file_json, indent=4), "Data/FlowGraphs/words/" + attribute + "s/" + attribute + ".json")
        f.write(minFile + "\n")


def create_word(word):
    minFile = "'Data/FlowGraphs/words/" + word + ".json','["
    for i, c in enumerate(word):
        if i == len(word) - 1:
            n = "null"
        else:
            n = str(i + 1)
        node = '[' + str(i) + ',"letter.json","letters/class_' + c + '.json",[' + n + ']],'
        minFile += node
    minFile = minFile[:-1]
    minFile += "]','[0]','[]','class:" + word + "'\n"

    with open("Data/FlowGraphs/flowGraphs.flowGraph", "a") as f:
        f.write(minFile)

    index = 0
    with open("Data/DataClasses/dataClasses.dataClass") as f:
        inputValues = csv.reader(f, delimiter=",", quotechar="\'")
        for value in inputValues:
            if int(value[1]) > index:
                    index = int(value[1])

    index += 1

    minDataClass = '"Data/DataClasses/words/' + word + '.json",' + str(index + 1) + ',"' + word + '","words/' + word + '.json"\n'

    with open("Data/DataClasses/dataClasses.dataClass", "a") as f:
        f.write(minDataClass)


def create_word_attribute(word, attribute):
    create_word(word)

    minFile = "'Data/FlowGraphs/words/" + attribute + "s/" + word + ".json','[[0,\"word.json\",\"words/" + word + ".json\",[null]]]','[0]','[]','" + attribute + ":" + word + "'\n"

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


refreshData()

#clean_json()

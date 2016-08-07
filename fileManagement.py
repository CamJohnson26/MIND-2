from Utilities.constructors import *
import json

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


def updateAdjectives():
    path = "Data/FlowGraphs/words/adjectives/"
    files = listdir(path)
    files = [f for f in files if isfile(join(path, f)) and f != 'adjective.json']

    file_json = {"graph": {"nodes": [], "guid": -1, "class": "GraphStructure", "name": "adjective"}, "contextNodes": [], "class": "FlowGraph", "startNodes": [] }
    for index, file in enumerate(files):
        node = {"dataClass": "words/" + file, "guid": index, "dataNode": "word.json", "class": "GraphNode", "nexts": [None] }
        file_json["graph"]["nodes"].append(node)
        file_json["startNodes"].append(index)

    with open("Data/FlowGraphs/flowGraphs.flowGraph", "a") as f:
        minFile = generateFlowGraphMinFile(json.dumps(file_json, indent=4), "Data/FlowGraphs/words/adjectives/adjective.json")
        f.write(minFile + "\n")


def updateAdverbs():
    path = "Data/FlowGraphs/words/adverbs/"
    files = listdir(path)
    files = [f for f in files if isfile(join(path, f)) and f != 'adverb.json']

    file_json = {"graph": {"nodes": [], "guid": -1, "class": "GraphStructure", "name": "adverb"}, "contextNodes": [], "class": "FlowGraph", "startNodes": [] }
    for index, file in enumerate(files):
        node = {"dataClass": "words/" + file, "guid": index, "dataNode": "word.json", "class": "GraphNode", "nexts": [None] }
        file_json["graph"]["nodes"].append(node)
        file_json["startNodes"].append(index)

    with open("Data/FlowGraphs/flowGraphs.flowGraph", "a") as f:
        minFile = generateFlowGraphMinFile(json.dumps(file_json, indent=4), "Data/FlowGraphs/words/adverbs/adverb.json")
        f.write(minFile + "\n")

def updateArticles():
    path = "Data/FlowGraphs/words/articles/"
    files = listdir(path)
    files = [f for f in files if isfile(join(path, f)) and f != 'article.json']

    file_json = {"graph": {"nodes": [], "guid": -1, "class": "GraphStructure", "name": "article"}, "contextNodes": [], "class": "FlowGraph", "startNodes": [] }
    for index, file in enumerate(files):
        node = {"dataClass": "words/" + file, "guid": index, "dataNode": "word.json", "class": "GraphNode", "nexts": [None] }
        file_json["graph"]["nodes"].append(node)
        file_json["startNodes"].append(index)

    with open("Data/FlowGraphs/flowGraphs.flowGraph", "a") as f:
        minFile = generateFlowGraphMinFile(json.dumps(file_json, indent=4), "Data/FlowGraphs/words/articles/article.json")
        f.write(minFile + "\n")


def updateConjunctions():
    path = "Data/FlowGraphs/words/conjunctions/"
    files = listdir(path)
    files = [f for f in files if isfile(join(path, f)) and f != 'conjunction.json']

    file_json = {"graph": {"nodes": [], "guid": -1, "class": "GraphStructure", "name": "conjunction"}, "contextNodes": [], "class": "FlowGraph", "startNodes": [] }
    for index, file in enumerate(files):
        node = {"dataClass": "words/" + file, "guid": index, "dataNode": "word.json", "class": "GraphNode", "nexts": [None] }
        file_json["graph"]["nodes"].append(node)
        file_json["startNodes"].append(index)

    with open("Data/FlowGraphs/flowGraphs.flowGraph", "a") as f:
        minFile = generateFlowGraphMinFile(json.dumps(file_json, indent=4), "Data/FlowGraphs/words/conjunctions/conjunction.json")
        f.write(minFile + "\n")


def updateNouns():
    path = "Data/FlowGraphs/words/nouns/"
    files = listdir(path)
    files = [f for f in files if isfile(join(path, f)) and f != 'noun.json']

    file_json = {"graph": {"nodes": [], "guid": -1, "class": "GraphStructure", "name": "noun"}, "contextNodes": [], "class": "FlowGraph", "startNodes": [] }
    for index, file in enumerate(files):
        node = {"dataClass": "words/" + file, "guid": index, "dataNode": "word.json", "class": "GraphNode", "nexts": [None] }
        file_json["graph"]["nodes"].append(node)
        file_json["startNodes"].append(index)

    with open("Data/FlowGraphs/flowGraphs.flowGraph", "a") as f:
        minFile = generateFlowGraphMinFile(json.dumps(file_json, indent=4), "Data/FlowGraphs/words/nouns/noun.json")
        f.write(minFile + "\n")


def updatePrepositions():
    path = "Data/FlowGraphs/words/prepositions/"
    files = listdir(path)
    files = [f for f in files if isfile(join(path, f)) and f != 'preposition.json']

    file_json = {"graph": {"nodes": [], "guid": -1, "class": "GraphStructure", "name": "preposition"}, "contextNodes": [], "class": "FlowGraph", "startNodes": [] }
    for index, file in enumerate(files):
        node = {"dataClass": "words/" + file, "guid": index, "dataNode": "word.json", "class": "GraphNode", "nexts": [None] }
        file_json["graph"]["nodes"].append(node)
        file_json["startNodes"].append(index)

    with open("Data/FlowGraphs/flowGraphs.flowGraph", "a") as f:
        minFile = generateFlowGraphMinFile(json.dumps(file_json, indent=4), "Data/FlowGraphs/words/prepositions/preposition.json")
        f.write(minFile + "\n")


def updateProperNouns():
    path = "Data/FlowGraphs/words/properNouns/"
    files = listdir(path)
    files = [f for f in files if isfile(join(path, f)) and f != 'properNoun.json']

    file_json = {"graph": {"nodes": [], "guid": -1, "class": "GraphStructure", "name": "properNoun"}, "contextNodes": [], "class": "FlowGraph", "startNodes": [] }
    for index, file in enumerate(files):
        node = {"dataClass": "words/" + file, "guid": index, "dataNode": "word.json", "class": "GraphNode", "nexts": [None] }
        file_json["graph"]["nodes"].append(node)
        file_json["startNodes"].append(index)

    with open("Data/FlowGraphs/flowGraphs.flowGraph", "a") as f:
        minFile = generateFlowGraphMinFile(json.dumps(file_json, indent=4), "Data/FlowGraphs/words/properNouns/properNoun.json")
        f.write(minFile + "\n")


def updateVerbs():
    path = "Data/FlowGraphs/words/verbs/"
    files = listdir(path)
    files = [f for f in files if isfile(join(path, f)) and f != 'verb.json']

    file_json = {"graph": {"nodes": [], "guid": -1, "class": "GraphStructure", "name": "verb"}, "contextNodes": [], "class": "FlowGraph", "startNodes": [] }
    for index, file in enumerate(files):
        node = {"dataClass": "words/" + file, "guid": index, "dataNode": "word.json", "class": "GraphNode", "nexts": [None] }
        file_json["graph"]["nodes"].append(node)
        file_json["startNodes"].append(index)

    with open("Data/FlowGraphs/flowGraphs.flowGraph", "a") as f:
        minFile = generateFlowGraphMinFile(json.dumps(file_json, indent=4), "Data/FlowGraphs/words/verbs/verb.json")
        f.write(minFile + "\n")


def refreshData():
    refreshDataTypes()
    refreshDataNodes()
    refreshDataClasses()
    refreshFlowGraphs()

    updateAdjectives()
    updateAdverbs()
    updateArticles()
    updateConjunctions()
    updateNouns()
    updatePrepositions()
    updateProperNouns()
    updateVerbs()

    refreshDataClasses()
    refreshFlowGraphs()


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


def create_adjective(word):
    create_word(word)

    minFile = "'Data/FlowGraphs/words/adjectives/" + word + ".json','[[0,\"word.json\",\"words/" + word + ".json\",[null]]]','[0]','[]','adjective:" + word + "'\n"

    with open("Data/FlowGraphs/flowGraphs.flowGraph", "a") as f:
        f.write(minFile)

    index = 0
    with open("Data/DataClasses/dataClasses.dataClass") as f:
        inputValues = csv.reader(f, delimiter=",", quotechar="\'")
        for value in inputValues:
            if int(value[1]) > index:
                    index = int(value[1])

    index += 1

    minDataClass = '"Data/DataClasses/words/adjectives/' + word + '.json",' + str(index) + ',"' + word + '","words/adjectives/' + word + '.json"\n'
    with open("Data/DataClasses/dataClasses.dataClass", "a") as f:
        f.write(minDataClass)


def create_adverb(word):
    create_word(word)

    minFile = "'Data/FlowGraphs/words/adverbs/" + word + ".json','[[0,\"word.json\",\"words/" + word + ".json\",[null]]]','[0]','[]','adverb:" + word + "'\n"

    with open("Data/FlowGraphs/flowGraphs.flowGraph", "a") as f:
        f.write(minFile)

    index = 0
    with open("Data/DataClasses/dataClasses.dataClass") as f:
        inputValues = csv.reader(f, delimiter=",", quotechar="\'")
        for value in inputValues:
            if int(value[1]) > index:
                    index = int(value[1])

    index += 1

    minDataClass = '"Data/DataClasses/words/adverbs/' + word + '.json",' + str(index) + ',"' + word + '","words/adverbs/' + word + '.json"\n'
    with open("Data/DataClasses/dataClasses.dataClass", "a") as f:
        f.write(minDataClass)


def create_article(word):
    create_word(word)

    minFile = "'Data/FlowGraphs/words/articles/" + word + ".json','[[0,\"word.json\",\"words/" + word + ".json\",[null]]]','[0]','[]','article:" + word + "'\n"

    with open("Data/FlowGraphs/flowGraphs.flowGraph", "a") as f:
        f.write(minFile)

    index = 0
    with open("Data/DataClasses/dataClasses.dataClass") as f:
        inputValues = csv.reader(f, delimiter=",", quotechar="\'")
        for value in inputValues:
            if int(value[1]) > index:
                    index = int(value[1])

    index += 1

    minDataClass = '"Data/DataClasses/words/articles/' + word + '.json",' + str(index) + ',"' + word + '","words/articles/' + word + '.json"\n'
    with open("Data/DataClasses/dataClasses.dataClass", "a") as f:
        f.write(minDataClass)


def create_conjunction(word):
    create_word(word)

    minFile = "'Data/FlowGraphs/words/conjunctions/" + word + ".json','[[0,\"word.json\",\"words/" + word + ".json\",[null]]]','[0]','[]','conjunction:" + word + "'\n"

    with open("Data/FlowGraphs/flowGraphs.flowGraph", "a") as f:
        f.write(minFile)

    index = 0
    with open("Data/DataClasses/dataClasses.dataClass") as f:
        inputValues = csv.reader(f, delimiter=",", quotechar="\'")
        for value in inputValues:
            if int(value[1]) > index:
                    index = int(value[1])

    index += 1

    minDataClass = '"Data/DataClasses/words/conjunctions/' + word + '.json",' + str(index) + ',"' + word + '","words/conjunctions/' + word + '.json"\n'
    with open("Data/DataClasses/dataClasses.dataClass", "a") as f:
        f.write(minDataClass)


def create_noun(word):
    create_word(word)

    minFile = "'Data/FlowGraphs/words/nouns/" + word + ".json','[[0,\"word.json\",\"words/" + word + ".json\",[null]]]','[0]','[]','noun:" + word + "'\n"

    with open("Data/FlowGraphs/flowGraphs.flowGraph", "a") as f:
        f.write(minFile)

    index = 0
    with open("Data/DataClasses/dataClasses.dataClass") as f:
        inputValues = csv.reader(f, delimiter=",", quotechar="\'")
        for value in inputValues:
            if int(value[1]) > index:
                    index = int(value[1])

    index += 1

    minDataClass = '"Data/DataClasses/words/nouns/' + word + '.json",' + str(index) + ',"' + word + '","words/nouns/' + word + '.json"\n'
    with open("Data/DataClasses/dataClasses.dataClass", "a") as f:
        f.write(minDataClass)


def create_preposition(word):
    create_word(word)

    minFile = "'Data/FlowGraphs/words/prepositions/" + word + ".json','[[0,\"word.json\",\"words/" + word + ".json\",[null]]]','[0]','[]','preposition:" + word + "'\n"

    with open("Data/FlowGraphs/flowGraphs.flowGraph", "a") as f:
        f.write(minFile)

    index = 0
    with open("Data/DataClasses/dataClasses.dataClass") as f:
        inputValues = csv.reader(f, delimiter=",", quotechar="\'")
        for value in inputValues:
            if int(value[1]) > index:
                    index = int(value[1])

    index += 1

    minDataClass = '"Data/DataClasses/words/prepositions/' + word + '.json",' + str(index) + ',"' + word + '","words/prepositions/' + word + '.json"\n'
    with open("Data/DataClasses/dataClasses.dataClass", "a") as f:
        f.write(minDataClass)


def create_properNoun(word):
    create_word(word)

    minFile = "'Data/FlowGraphs/words/properNouns/" + word + ".json','[[0,\"word.json\",\"words/" + word + ".json\",[null]]]','[0]','[]','properNoun:" + word + "'\n"

    with open("Data/FlowGraphs/flowGraphs.flowGraph", "a") as f:
        f.write(minFile)

    index = 0
    with open("Data/DataClasses/dataClasses.dataClass") as f:
        inputValues = csv.reader(f, delimiter=",", quotechar="\'")
        for value in inputValues:
            if int(value[1]) > index:
                    index = int(value[1])

    index += 1

    minDataClass = '"Data/DataClasses/words/properNouns/' + word + '.json",' + str(index) + ',"' + word + '","words/properNouns/' + word + '.json"\n'
    with open("Data/DataClasses/dataClasses.dataClass", "a") as f:
        f.write(minDataClass)


def create_verb(word):
    create_word(word)

    minFile = "'Data/FlowGraphs/words/verbs/" + word + ".json','[[0,\"word.json\",\"words/" + word + ".json\",[null]]]','[0]','[]','verb:" + word + "'\n"

    with open("Data/FlowGraphs/flowGraphs.flowGraph", "a") as f:
        f.write(minFile)

    index = 0
    with open("Data/DataClasses/dataClasses.dataClass") as f:
        inputValues = csv.reader(f, delimiter=",", quotechar="\'")
        for value in inputValues:
            if int(value[1]) > index:
                    index = int(value[1])

    index += 1

    minDataClass = '"Data/DataClasses/words/verbs/' + word + '.json",' + str(index) + ',"' + word + '","words/verbs/' + word + '.json"\n'
    with open("Data/DataClasses/dataClasses.dataClass", "a") as f:
        f.write(minDataClass)

# pns = ["lacey","lauren","hamilton"]
# for pn in pns:
#     create_properNoun(pn)

refreshData()

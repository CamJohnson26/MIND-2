from Utilities.constructors import *
from fileManagement import *
from os.path import join

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


def create_word_dataClass(word, pos):
    dcfm = DataClassFileManager()
    dc_json = json.loads('''{
                                "dataClassIndex": ''' + str(dcfm.get_next_index()) + ''',
                                "dataClasses": {
                                    "partOfSpeech": "words/partOfSpeech/''' + pos + '''.json"
                                },
                                "dataClassString": "''' + word.lower() + '''",
                                "class": "DataClass",
                                "flowGraph": "words/''' + word.lower() + '''.json"
                            }''')
    file = join(dcfm.home_folder, "words/dataIndex/" + word.lower() + "-" + pos + ".json")
    minFile = dcfm.json_to_min_file(json.dumps(dc_json), file)
    dcfm.add_minObject_to_file(minFile)

def create_word_flowGraph(word):
    fgfm = FlowGraphFileManager()
    flow_json = json.loads("""{
                                    "graph": {
                                        "nodes": [
                                        ],
                                        "guid": -1,
                                        "class": "GraphStructure",
                                        "name": "class:""" + word.lower() + """\"
                                    },
                                    "contextNodes": [],
                                    "class": "FlowGraph",
                                    "startNodes": [
                                        0
                                    ]
                                }""")

    for i, c in enumerate(word.lower()):
        next_ind = str(i + 1 if i < (len(word) - 1) else "null")
        letter_json = json.loads("""{
                                        "dataClasses": {
                                            "dataIndex": "letters/dataIndex/class_""" + c + """.json"
                                        },
                                        "dataNode": "letter.json",
                                        "nexts": [
                                            """ + next_ind + """
                                        ],
                                        "dataClass": null,
                                        "guid": """ + str(i) + """,
                                        "class": "GraphNode"
                                    }""")

        flow_json["graph"]["nodes"].append(letter_json)
    file = join(fgfm.home_folder, "words/" + word.lower() + ".json")
    minFile = fgfm.json_to_min_file(json.dumps(flow_json), file)
    fgfm.add_minObject_to_file(minFile)


def create_noun(word):
    create_word_flowGraph(word)
    create_word_dataClass(word, "noun")


def create_verb(word):
    create_word_flowGraph(word)
    create_word_dataClass(word, "verb")


def create_adjective(word):
    create_word_flowGraph(word)
    create_word_dataClass(word, "adjective")


def create_adverb(word):
    create_word_flowGraph(word)
    create_word_dataClass(word, "adverb")


def create_article(word):
    create_word_flowGraph(word)
    create_word_dataClass(word, "article")


def create_conjunction(word):
    create_word_flowGraph(word)
    create_word_dataClass(word, "conjunction")


def create_preposition(word):
    create_word_flowGraph(word)
    create_word_dataClass(word, "preposition")


def create_properNoun(word):
    create_word_flowGraph(word)
    create_word_dataClass(word, "properNoun")


create_adverb("like")
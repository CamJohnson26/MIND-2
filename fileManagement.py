from Utilities.constructors import *
from Utilities.dataClassFileManager import DataClassFileManager
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

dtfm = DataTypeFileManager()
dnfm = DataNodeFileManager()
dcfm = DataClassFileManager()
fgfm = FlowGraphFileManager()

def refreshData():
    dtfm.refreshObjects()
    dnfm.refreshObjects()
    dcfm.refreshObjects()
    fgfm.refreshObjects()

    dcfm.refreshObjects()
    fgfm.refreshObjects()


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


def save_all_folders():
    dtfm = DataTypeFileManager()
    dnfm = DataNodeFileManager()
    dcfm = DataClassFileManager()
    fgfm = FlowGraphFileManager()

    dtfm.save_home_folder_to_min_file()
    dnfm.save_home_folder_to_min_file()
    dcfm.save_home_folder_to_min_file()
    fgfm.save_home_folder_to_min_file()


if __name__ == '__main__':
    #save_all_folders()
    clean_json()
    refreshData()
    # print(dnfm.objectFromJSON("""{
    #     "dataType": "letter.json", 
    #     "parsedData": "E", 
    #     "class": "DataNode", 
    #     "dataClasses": {}
    # }"""))
    #print(dcfm.min_file_to_json("'abcdefg',0,'adjective',,'{}'"))
    # 'abcdefg',0,'adjective',,'{}'

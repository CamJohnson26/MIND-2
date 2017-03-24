import json
import os



folder = os.path.abspath(os.path.join(os.path.dirname( "Data" ), '..'))
data_index = ""
for dirName, subdirList, fileList in os.walk(folder):
    for file in fileList:
        if file.endswith(".json"):
            data_index += "file:\\\\\\" + os.path.join(dirName, file) + "\n"

f = open('data_index.txt', 'r+')
f.truncate()
f.write(data_index);
f.close()

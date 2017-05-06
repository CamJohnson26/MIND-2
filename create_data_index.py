import os


folder = os.path.join("MIND2", os.path.dirname("Data"))
data_index = ""
for dirName, subdirList, fileList in os.walk(folder):
    for file in fileList:
        if file.endswith(".json"):
            data_index += os.path.join(dirName, file).replace("\\", "/") + "\n"

f = open('data_index.txt', 'r+')
f.truncate()
f.write(data_index)
f.close()

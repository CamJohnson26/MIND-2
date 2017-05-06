import os
import shutil

root = "C:\\Users\\Cameron\\Desktop\\Sort This\\MIND2\\MIND2\\Data\\Core\\level2\\word\\classes\\dataIndex"
folders = os.listdir(root)

for f in folders:
	if ".json" in f:
		shutil.rmtree(os.path.join(root, f))
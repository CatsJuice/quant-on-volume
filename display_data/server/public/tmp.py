import os
from tqdm import tqdm

filelist = os.listdir("./dayline/")

# print(filelist)
for i in tqdm(range(len(filelist))):
    file = filelist[i]
    f = open("./dayline/%s" % file ,"r", encoding="utf-8")
    content = f.read()
    w = open("./dayline/%s" % file ,"w", encoding="utf-8")
    w.write(content.replace("module.exports = =", "module.exports ="))
    f.close()
    w.close()
    # break

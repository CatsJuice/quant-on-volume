import os
import sys

import pandas as pd

codeList = os.listdir("E:\\files\\stock\\dayline\\with_my_result\\")

for filename in codeList:
    f = open(sys.path[0].replace("script", "src") + "\\data\\dayline\\%s.js"%filename[0:6], "w", encoding="utf-8")
    f.write('''module.exports  [
    ''')
    try:
        df = pd.read_csv("E:\\files\\stock\\dayline\\with_my_result\\" + filename, encoding="gbk",  error_bad_lines=False, index_col=0)
    except:
        print("ERROR ORENING %s" % filename)
    for index, row in df.iterrows():
        # print(list(row.items()))
        f.write('''%s,
        ''' % row.to_dict())
    f.write("]")
    f.close()
    # break
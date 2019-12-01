import os
import sys


codeList = os.listdir("E:\\files\\stock\\dayline\\with_my_result\\")
f = open(sys.path[0].replace("script", "src") + "\\data\\code_list.js", "w", encoding="utf-8")
f.write('''export default  [
    ''')
for filename in codeList:
    f.write('''"%s",
    ''' % filename[0:6])
f.write("]")
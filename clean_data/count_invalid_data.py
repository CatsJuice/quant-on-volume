import os
import sys
import json
import pandas as pd
import time
from tqdm import tqdm

class CountInvalidData(object):

    def __init__(self, end_date="20140101"):
        const_path = sys.path[0].replace("\\clean_data", "")
        f = open(const_path + "\\const.json", "r", encoding="utf8")
        self.consts = json.loads(f.read())
        self.end_date = end_date
        self.day_line_file_prefix = self.consts["day_line_file_prefix"]["netease"]
        self.COUNT_INVALID_DATA = 0
        self.COUNT_INVALID_CODE = 0

    def handle_one(self, code):
        try:
            df = pd.read_csv("%s%s.csv" % (self.day_line_file_prefix, code), encoding="gbk", error_bad_lines=False)
        except:
            print("ERROR While Opening Code %s" % code )
            return
        all_right = True
        for index,row in df.iterrows():
            if row['日期'] < self.end_date: break
            flag = True     # 标记是否有效
            # 遍历行中的每一项
            for i,val in row.items():
                if val == "None" or val == "NaN" or (val == 0 and (i[:2] != '涨跌')):
                    flag = False
                    all_right = False
                    self.COUNT_INVALID_DATA += 1
                    break
            
        if not all_right:
            self.COUNT_INVALID_CODE += 1

    
    def handle_all(self):
        time_start = time.time() 
        file_list = os.listdir(self.day_line_file_prefix)
        file_count = len(file_list)
        for i in tqdm(range(file_count)):
            file = file_list[i]
            code = file[0:6]
            self.handle_one(code)
            # time.sleep(1)
        print("无效的数据数量：", self.COUNT_INVALID_DATA)      
        print("有无效数据的股票数量：", self.COUNT_INVALID_CODE)
        time_end = time.time()
        time_c= time_end - time_start   #运行所花时间
        print('time cost:', time_c, 's')


if __name__ == "__main__":
    cid = CountInvalidData()
    cid.handle_all()
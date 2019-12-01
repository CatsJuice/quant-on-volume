import os
import sys
import pandas as pd
import json
import time
from tqdm import tqdm

class HandleNaN(object):

    def __init__(self):
        const_path = sys.path[0].replace("\\clean_data", "")
        f = open(const_path + "\\const.json", "r", encoding="utf8")
        self.consts = json.loads(f.read())

        self.dayline_file_prefix = self.consts["day_line_file_prefix"]['netease']

    def handle_one(self,code):
        try:
            df = pd.read_csv("%s%s.csv" % (self.dayline_file_prefix, code), encoding="gbk")
        except:
            print("error")
            return
        df = df[df['日期'] > "20140101"]
        return df.isna().any().any()

    def handle_all(self):
        time_start = time.time()
        file_list = os.listdir(self.dayline_file_prefix)
        for i in tqdm(range(len(file_list))):
            if self.handle_one(file_list[i][0:6]): print(file_list[i])
        time_end = time.time()
        time_c= time_end - time_start
        print("Finished! Take %s Seconds" % time_c)


if __name__ == "__main__":
    hn = HandleNaN()
    hn.handle_all()
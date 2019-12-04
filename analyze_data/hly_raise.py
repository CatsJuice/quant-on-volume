import sys
import os
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
from collections import deque
import copy

class Raise(object):

    def __init__(self, day_arr=[5,6,7,8,9,10,11,12], ma_arr=[5,6,7,8,9,10,10]):
        const_path = sys.path[0].replace("\\analyze_data", "")
        f = open(const_path + "\\const.json", "r", encoding="utf8")
        self.consts = json.loads(f.read())
        self.dayline_file_prefix = self.consts['day_line_file_prefix']['netease_clean']
        self.with_my_result = self.consts['path']['result']['hly']

        self.day_arr = day_arr
        self.ma_arr = ma_arr
        self.res_up = {}
        self.res_down = {}

    def one(self, code):
        try:
            df = pd.read_csv("%s%s.csv" % (self.with_my_result, code), encoding="gbk")
        except:
            print("ERROR %s " % code)
            return
        sum_arr = {}
        for index, row in df[::-1].iterrows():
            for day in self.day_arr:
                if day in sum_arr.keys():
                    sum_arr[day].append(row['hly_score'])
                    if len(sum_arr[day]) < day:
                        continue
                    if index-5 >= 0:
                        if (self.isRaise(sum_arr[day], type=2)):    # 满足形态
                            self.updateRes(row['ma_5'] > df.loc[index-5, 'ma_5'], day)
                        sum_arr[day].popleft()
                        # for ma in self.ma_arr:
                        #     self.updateRes(row['ma_%s' % ma] > df.loc[index-ma, 'ma_%s' % ma], day, ma)
                    else:
                        return
                else:
                    sum_arr[day] = deque([row['hly_score']])

    def all(self):
        filelist = os.listdir(self.with_my_result)
        for i in tqdm(range(len(filelist))):
            code = filelist[i][0:6]
            self.one(code)
            # print(self.res_up)
            # print(self.res_down)
        f = open("%s\\hly_count_res_ma5_type_1_up.json" % sys.path[0], "w", encoding="utf-8")
        f.write(json.dumps(self.res_up, ensure_ascii=False))
        f.close()

        f = open("%s\\hly_count_res_ma5_type_1_down.json" % sys.path[0], "w", encoding="utf-8")
        f.write(json.dumps(self.res_down, ensure_ascii=False))
        f.close()


    def isRaise(self, arr, type):
        c = copy.deepcopy(arr)
        c.popleft()
        if type == 1:
            for item in c:
                if item <= 0:
                    return False
            return True
        if type == 2:
            x = np.array(list(range(len(arr))))
            y = np.array(arr)
            line = np.polyfit(x, y, deg=1)
            return line[0] > 0
    
    def updateRes(self, flag, day):
        key = "_%s"%day
        if flag:
            if not key in self.res_up.keys():
                self.res_up[key] = 0
            self.res_up[key] += 1
        else:
            if not key in self.res_down.keys():
                self.res_down[key] = 0
            self.res_down[key] += 1

if __name__ == "__main__":
    r = Raise()
    r.all()
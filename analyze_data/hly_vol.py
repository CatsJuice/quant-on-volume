import sys
import json
import pandas as pd
import time
import os

from tqdm import tqdm
from functools import reduce
from collections import deque

class HlyScore(object):

    def __init__(self, serial_day_arr=[7]):
        const_path = sys.path[0].replace("\\analyze_data", "")
        f = open(const_path + "\\const.json", "r", encoding="utf8")
        self.consts = json.loads(f.read())
        self.dayline_file_prefix = self.consts['day_line_file_prefix']['netease_clean']
        self.with_my_result = self.consts['day_line_file_prefix']['with_my_result']

        self.serial_day_arr = serial_day_arr    # 连续计算的天数

    # 计算单只股票的加分
    def calculate_score_one(self,code):
        column_name = 'hly_score'
        try:
            df = pd.read_csv("%s%s.csv" % (self.dayline_file_prefix, code), encoding="gbk", error_bad_lines=False)
        except:
            print("ERROR WHILE OPENING %s.csv" % code)
        df = df[::-1]
        df[column_name] = ""
        last_row = pd.Series([])
        for index,row in df.iterrows():
            if last_row.empty: score = 0
            else: score = self.get_score(last_row,row)
            df.loc[index, column_name] = score
            last_row = row
        df[::-1].to_csv("%s%s.csv" % (self.with_my_result, code), encoding="gbk", index=None)
            
    def calculate_score_all(self):
        time_start = time.time() 
        file_list = os.listdir(self.dayline_file_prefix)
        file_count = len(file_list)
        for i in tqdm(range(file_count)):
            file = file_list[i]
            code = file[0:6]
            self.calculate_score_one(code)
        time_end = time.time()
        time_c= time_end - time_start   #运行所花时间
        print('time cost: %s Seconds' % time_c)
        
    # 计算单只股票的加分和
    def calculate_sum_one(self, code):
        colmun_name = "sum_%s"
        try:
            df = pd.read_csv("%s%s.csv" % (self.with_my_result, code), encoding="gbk", error_bad_lines=False)
        except:
            print("ERROR WHILE OPENING %s.csv" % code)
        sum_arr = {}
        for sum in self.serial_day_arr:
            df[colmun_name % sum] = ""
            sum_arr[sum] = deque([])

        df = df[::-1]
        for index,row in df.iterrows():
            for day in sum_arr:
                if len(sum_arr[day]) < int(day):
                    sum_arr[day].append(row['hly_score'])
                    df.loc[index,colmun_name % day] = 0
                else:
                    sum_arr[day].popleft()
                    sum_arr[day].append(row['hly_score'])
                    df.loc[index,colmun_name % day] = reduce(lambda x,y:x+y,sum_arr[day])
        df[::-1].to_csv("%s%s.csv" % (self.with_my_result, code), encoding="gbk",index=None)

    def calculate_sum_all(self):
        time_start = time.time() 
        file_list = os.listdir(self.dayline_file_prefix)
        file_count = len(file_list)
        for i in tqdm(range(file_count)):
            file = file_list[i]
            code = file[0:6]
            self.calculate_sum_one(code)
        time_end = time.time()
        time_c= time_end - time_start   #运行所花时间
        print('time cost: %s Seconds' % time_c)

    def get_score(self,yesterday,today):
        if yesterday['收盘价'] < today['收盘价']:
            if yesterday['成交量'] < today['成交量']:
                return 2
            else:
                return 1
        elif yesterday['收盘价'] > today['收盘价']:
            if yesterday['成交量'] < today['成交量']:
                return -2
            else:
                return -1
        return 0

if __name__ == "__main__":
    hly = HlyScore(serial_day_arr=[6,7,8,9,10])
    # hly.calculate_score_all()
    # hly.calculate_sum_one('000002')
    hly.calculate_sum_all()
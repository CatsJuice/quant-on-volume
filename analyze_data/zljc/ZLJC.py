import os
import sys
import json
import pandas as pd
import numpy as np
from collections import deque
from tqdm import tqdm

class ZLJCCalc(object):

    def __init__(self):
        const_path = sys.path[0].replace("\\analyze_data\\zljc", "")
        f = open(const_path + "\\const.json", "r", encoding="utf8")
        self.consts = json.loads(f.read())
        
        self.day_line_file_prefix = self.consts['day_line_file_prefix']['netease']
        self.data_clean_prefix = self.consts['day_line_file_prefix']['netease_clean'] + "new\\"
        self.zljc_path = self.consts['path']['result']['zljc']

    def var1(self, close, low, high):
        return (close + low + high) / 3

    def var2(self, var1, ref_low_1, high, vol, low, var2_yesterday):
        division = 1 if high == low else high - low
        var2_today = ((var1 - ref_low_1) - (high - var1)) * (vol / 100) / 100000 / division
        return float(var2_yesterday) + float(var2_today)

    def ma(self, arr):
        res = 0
        for i in arr:
            res += i
        return res / len(arr)

    def zljc(self, df):
        M = 12
        L = 26
        df['JCS'] = ""
        df['JCM'] = ""
        df['JCL'] = ""

        ma_jcm = deque([])
        ma_jcl = deque([])
        sum_jcm = 0
        sum_jcl = 0

        yesterday = pd.DataFrame([])
        for index, row in df[::-1].iterrows():
            var1 = self.var1(row['收盘价'], row['最低价'], row['最高价'])
            if yesterday.empty:
                df.loc[index, "JCS"] = self.var2(var1, row['最低价'], row['最高价'], row['成交量'], row['最低价'], 0)
                df.loc[index, "JCM"] = 0
                df.loc[index, "JCL"] = 0
            else:
                var3 = self.var2(var1, yesterday['最低价'], row['最高价'], row['成交量'], row['最低价'], yesterday['JCS'])
                df.loc[index, "JCS"] = var3
                ma_jcm.append(var3)
                ma_jcl.append(var3)
                sum_jcm += var3
                sum_jcl += var3
                if len(ma_jcm) < M:     # 不够计算 MA
                    df.loc[index, "JCM"] = 0
                else:   # 计算 MA
                    df.loc[index, "JCM"] = sum_jcm / M
                    sum_jcm -= ma_jcm.popleft()

                if len(ma_jcl) < L:     # 不够计算 MA
                    df.loc[index, "JCL"] = 0
                else:   # 计算 MA
                    df.loc[index, "JCL"] = sum_jcl / L
                    sum_jcl -= ma_jcl.popleft()
            yesterday = df.loc[index]
        return df


    def handle_one(self, code):
        try:
            # df = pd.read_csv("%s%s.csv" % (self.day_line_file_prefix, code), encoding="gbk")
            df = pd.read_csv("%s%s.csv" % (self.data_clean_prefix, code), encoding="gbk")
        except:
            print("\nERROR OPEING %s.csv")
            return 
        df = self.zljc(df)
        df.to_csv("%s%s.csv" % (self.zljc_path, code), encoding="gbk",index=None)

    def handle_all(self):
        filelist = os.listdir(self.data_clean_prefix)
        for i in tqdm(range(len(filelist))):
            code = filelist[i][0:6]
            self.handle_one(code)

    def module_export(self):
        for file in os.listdir(self.zljc_path):
            try:
                df = pd.read_csv(self.zljc_path + file , encoding="gbk")
            except:
                print("ERROR OPENING %s" % file)
                continue
            f = open("%sjs\\%s.js" %(self.zljc_path, file[0:6]),"w", encoding="utf-8")
            f.write('''module.exports=[
                        ''')
            for index,row in df.iterrows():
                f.write('''{
                    date: '%s',
                    jcs: %.2f,
                    jcm: %.2f,
                    jcl: %.2f,
                },''' % (row['日期'], row['JCS'], row['JCM'], row['JCL']))
            f.write('''
            ]''')
            f.close()

if __name__ == "__main__":
    zljc = ZLJCCalc()
    # zljc.handle_one('000001')
    zljc.handle_all()
    # zljc.module_export()
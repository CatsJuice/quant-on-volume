import sys
import json
import pandas as pd
import tushare as ts
import os
from tqdm import tqdm

import time
import random

class DataClean(object):

    def __init__(self, end_date="20140101"):
        const_path = sys.path[0].replace("\\clean_data", "")
        f = open(const_path + "\\const.json", "r", encoding="utf8")
        self.consts = json.loads(f.read())

        self.end_date = end_date
        self.tushare_token = self.consts["tushare"]["token"]
        self.day_line_file_prefix = self.consts["day_line_file_prefix"]["netease"]
        self.COUNT_INVALID_DATA = 0
        self.COUNT_INVALID_CODE = 0

    # 处理单只股票
    def handle_one(self, code):
        # handled = self.is_handled(code)
        # if handled: return
        try:
            df = pd.read_csv("%s%s.csv" % (self.day_line_file_prefix, code), encoding="gbk", error_bad_lines=False)
        except:
            print("ERROR While Opening Code %s" % code )
            return
        newData = pd.DataFrame([],columns=df.columns)
        codeInfo = pd.Series([])
        for index,row in df.iterrows():
            if row['日期'] < self.end_date: continue
            flag = True     # 标记是否有效
            new_row = row
            # 遍历行中的每一项
            for i,val in row.items():
                if val == "None" or val == "NaN" or (val == 0 and (i[:2] != '涨跌')):
                    flag = False
                    if codeInfo.empty:
                        try:
                            codeInfo = pd.read_csv("%s%s.csv"%(self.consts['day_line_file_prefix']['tushare'], code), encoding="gbk")
                        except:
                            print("打开tushare %s失败" % code)
                    invalid_date = "".join(row['日期'].split("-"))
                    try:
                        tushare_row = codeInfo.loc[codeInfo['trade_date']==invalid_date]
                    except:
                        tushare_row = pd.Series([])
                    if not tushare_row.empty:       # tushare 有这一天的数据
                        new_row = pd.Series([
                            row['日期'],     # 日期
                            row['股票代码'],  # 股票代码
                            row['名称'], # 名称
                            tushare_row['close'],   # 收盘价
                            tushare_row['high'],    # 最高价
                            tushare_row['low'],    # 最低价
                            tushare_row['open'],    # 开盘价
                            tushare_row['prev_close'],    # 前收盘
                            tushare_row['change'],    # 涨跌额
                            tushare_row['pct_chg'],    # 涨跌幅
                            0,    # 换手率
                            tushare_row['vol'],    # 成交量
                            tushare_row['amount'],    # 成交额
                            row['总市值'],    # 总市值
                            row['流通市值'],    # 流通市值
                        ], columns=df.columns)
                        newData.loc[len(newData.index)] = new_row
                    break   # 该行以发现无效数据， 整行处理， 不继续遍历改行的剩余元素
            if (not flag):
                # print("[%s.csv] 在 [%s] 数据无效;" % (code, row['日期']))
                self.COUNT_INVALID_DATA += 1 # 埋点，统计无效的数据数量
            else:
                newData.loc[len(newData.index)] = row
        
        if not codeInfo.empty: self.COUNT_INVALID_CODE+=1        # 埋点，统计无效的股票数量
        newData.to_csv('%s%s.csv'%(self.consts['day_line_file_prefix']['netease_clean'], code), encoding="gbk")

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
        print('time cost: %s Seconds' % time_c)

    def is_handled(self, code):
        try:
            df = pd.read_csv('%s%s.csv'%(self.consts['day_line_file_prefix']['netease_clean'], code), encoding="gbk")
            return True
        except:
            return False

if __name__ == "__main__":
    data_clean = DataClean()
    # data_clean.handle_one('000503')
    data_clean.handle_all()

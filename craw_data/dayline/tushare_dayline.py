import sys
import json
import pandas as pd
import tushare as ts
import os
from tqdm import tqdm

import time
import random

const_path = sys.path[0].replace("craw_data\\dayline", "")
f = open(const_path + "\\const.json", "r", encoding="utf8")
consts = json.loads(f.read())
ts.set_token(consts["tushare"]["token"])
pro = ts.pro_api()

class TuShareDayline(object):

    def __init__(self,start_date="20140101", end_date="20191111"):
        const_path = sys.path[0].replace("craw_data\\dayline", "")
        f = open(const_path + "\\const.json", "r", encoding="utf8")
        self.consts = json.loads(f.read())

        self.start_date = start_date
        self.end_date = end_date
        self.stock_list_prefix = self.consts['path']['stock_list']['tushare']
        self.tushare_token = self.consts["tushare"]["token"]
        self.day_line_file_prefix = self.consts["day_line_file_prefix"]["tushare"]
        

    def craw_one(self, code):
        if self.check_is_downloaded(code): 
            print("%s已下载"%code) 
            return
        try:
            codeInfo = pro.daily(ts_code=code, start_date=self.start_date, end_date=self.end_date)
            codeInfo.to_csv('%s%s.csv'%(self.day_line_file_prefix,code[0:6]), encoding="gbk", index=0)
            return True
        except:
            print("调用接口失败")
            for i in range(60):
                print("SLEEPING.....................%s" % (60-i))
                time.sleep(1)
            return False
        
            

    def check_is_downloaded(self, code):
        file_list = os.listdir(self.day_line_file_prefix)
        return (code[0:6] + ".csv") in file_list

    def get_all(self):
        df = pd.read_csv(self.stock_list_prefix+'\\tushare.csv', encoding="gbk")
        count = df.index.size

        LIMIT = 100

        for index,row in df.iterrows():
            print("%s/%s-----------%s" % (index+1, count, (index+1)/count))
            completed = self.craw_one(row['ts_code'])
            if LIMIT == 0:
                LIMIT = 100
                for i in range(60):
                    print("SLEEPING.....................%s" % (60-i))
                    time.sleep(1)
            if completed: LIMIT -= 1

if __name__ == "__main__":
    tsd  = TuShareDayline()
    # tsd.craw_one('000001')
    tsd.get_all()
import sys
from download import download
import json
import time
import random

import pandas as pd
from tqdm import tqdm

request_params = [
    { "key":"rtntype",
      "value":"5",
      "equals":True,
      "description":"",
      "enabled":True 
    },
      
    { "key":"token",
      "value":"4f1862fc3b5e77c150a2b985b12db0fd",
      "equals":True,
      "description":"",
      "enabled":True 
    },
      
    { "key":"cb",
      "value":"jQuery1124036208821942748104_1574562443091",
      "equals":True,
      "description":"",
      "enabled":True 
    },
      
    { "key":"id",
      "value":"%s",
      "equals":True,
      "description":"",
      "enabled":True 
    },
      
    { "key":"type",
      "value":"k",
      "equals":True,
      "description":"",
      "enabled":True 
    },
      
    { "key":"authorityType",
      "value":"",
      "equals":True,
      "description":"",
      "enabled":True 
    },
      
    { "key":"_",
      "value":"1574509941411",
      "equals":True,
      "description":"",
      "enabled":True}
]
URI = "http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?"

for param in request_params:
    URI += '%s=%s&' % (param["key"], param["value"])

class EastMoneyDayLine(object):

    def __init__(self, end_date='00000000'):

        const_path = sys.path[0].replace("\\craw_data\\dayline", "")
        f = open(const_path + "\\const.json", "r", encoding="utf8")
        self.consts = json.loads(f.read())

        self.stock_list_file = self.consts['stock_list_file']                        # 全部股票信息的csv文件
        self.save_path_prefix = self.consts['day_line_file_prefix']['ease_money']    # 日线存储文件夹目录
        self.end_date = end_date                                                     # 截止日期
        self.codes = self.get_codes()

        self.downloader = download.Downloader()                                      # 下载器

    def craw_one(self, code):
        url = URI % self.process_code(code)
        content = self.handle_jsonp(self.downloader.requests_get(url, type="json").decode("utf8"))
        # print(content)
        data = json.loads(content)
        self.save_json_to_csv(data, code)

    def get_codes(self):
        try:
            df = pd.read_csv(self.stock_list_file, encoding="gbk", error_bad_lines=False)
        except:
            print("ERROR Opening File: %s" % self.stock_list_file)
            return False
        
        codes = []
        for index, row in df.iterrows():
            codes.append(row['股票代码'][1:])
        return codes

    def save_json_to_csv(self, data, code):
        realdata = data['data']
        f = open(self.save_path_prefix + str(code) + ".csv", "w", encoding="gbk")
        f.write(",".join(['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅']))
        f.write("\n")
        for row in realdata[:-1]:
            if ("".join(row[:10].split("-")) < self.end_date): continue
            f.write(row[:-2])
            f.write("\n")
        f.close()

    def process_code(self, code):
        return '%s1' % code

    def handle_jsonp(self, response_content):
        return response_content[response_content.find("{"):-1]

    def check_is_downloaded(self, code):
        try:
            df = pd.read_csv(self.save_path_prefix + code + ".csv")
            return True
        except:
            return False
        

    def controller(self):
        for i in tqdm(range(len(self.codes))):
            code = self.codes[i]
            if (self.check_is_downloaded(code)) return 
            self.craw_one(code)
            time.sleep(random.random()*2)


if __name__ == "__main__":
    east_money_day_line = EastMoneyDayLine()
    east_money_day_line.controller()
    # east_money_day_line.craw_one(600175)      # test craw
import tushare as ts
import pandas as pd
import sys
import json

const_path = sys.path[0].replace("craw_data\\stock_list", "")
f = open(const_path + "\\const.json", "r", encoding="utf8")
consts = json.loads(f.read())

ts.set_token(consts["tushare"]["token"])
pro = ts.pro_api()
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

data.to_csv(consts['path']['stock_list']['tushare'] +'\\tushare.csv', encoding="gbk")
with open(consts['path']['stock_list']['tushare'] +'\\tushare.json', 'w', encoding='utf-8') as file:     
    data.to_json(file, orient="records", lines=True, force_ascii=False)
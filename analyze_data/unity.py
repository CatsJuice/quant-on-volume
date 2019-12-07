import sys
import json
import pandas as pd

class Unity(object):

    def __init__(self):
        const_path = sys.path[0].replace("\\analyze_data", "")
        f = open(const_path + "\\const.json", "r", encoding="utf8")
        self.consts = json.loads(f.read())

    def do(self):
        f1 = open(sys.path[0] + "\\hly_count_res_max_4_group_by_date.json", "r", encoding="utf-8")
        hly = json.loads(f1.read())
        
        f2 = open(sys.path[0] + "\\zljc\\zljc_day_a.json", "r", encoding="utf-8")
        zljc = json.loads(f2.read())

        res = {}
        for code in zljc:
            for a in zljc[code]:
                for day in zljc[code][a]:
                    for date in zljc[code][a][day]["dates_yes"]:
                        # 筛选 hly 中该日期的股票有没有当前这只
                        if date in hly.keys() and code in hly[date]:
                            if date not in res.keys(): res[date] = []
                            if code not in res[date]: res[date].append(code)

        
        f3 = open(sys.path[0] + "\\hly_and_zljc_res.json", "w", encoding="utf-8")
        f3.write(json.dumps(res, ensure_ascii=False))
        f3.close()
        f2.close()
        f1.close()

    def verify(self):
        f = open(sys.path[0] + "\\hly_and_zljc_res.json", "r", encoding="utf-8")
        res = json.loads(f.read())
        transform_dic = {}
        for date in res:
            for code in res[date]:
                if code not in transform_dic:
                    transform_dic[code] = []
                transform_dic[code].append(date)
        # f3 = open(sys.path[0] + "\\hly_and_zljc_res_transform.json", "w", encoding="utf-8")
        # f3.write(json.dumps(transform_dic, ensure_ascii=False))
        # f3.close()

        count = {
            "yes": 0,
            "no": 0
        }
        for code in transform_dic:
            print(code)
            try:
                df = pd.read_csv("%s%s.csv" %  (self.consts['path']['result']['hly'], code), encoding="gbk")
            except:
                print("ERROR OPENING %s" % code)
                continue
            for index, row in df.iterrows():
                if row['日期'] in transform_dic[code]:
                    if index - 5 > 0:
                        if df.loc[index-5, "收盘价"] > row["收盘价"]:
                            count["yes"] += 1
                        else:
                            count["no"] += 1

        print(count)

if __name__ == "__main__":
    u = Unity()
    # u.do()
    u.verify()
import sys
import os
import pandas as pd
import json
from tqdm import tqdm

class Verify(object):

    def __init__(self):
        const_path = sys.path[0].replace("\\analyze_data", "")
        f = open(const_path + "\\const.json", "r", encoding="utf8")
        self.consts = json.loads(f.read())
        self.with_my_result = self.consts['path']['result']['hly']
        self.res = {}

    def verify_one(self, code, dscore):
        # 找出数据最新的一天的连续计算打分最高的数据
        # 如果是 sum_5 就找得分为 9，10 的， 以此类推
        try:
            df = pd.read_csv('%s%s.csv' % (self.with_my_result, code), encoding="gbk")
        except:
            print("ERROR %s" % code)
            return
        columns = df.columns
        sum_arr = []
        # print("HANDLE %s ..." % code)
        for col in columns:
            if col[0:3] == "sum":
                sum_arr.append(int(col[4:]))
        for index,row in df.iterrows():
            for s in sum_arr:
                if row["sum_%s" % s] == s*2 - dscore:
                    if (row['日期'] in self.res.keys()):
                        self.res[row['日期']].append(code)
                    else:
                        self.res[row['日期']] = [code]
                    break
            

    def verify_all(self, dscore=2):
        files = os.listdir(self.with_my_result)
        for i in tqdm(range(len(files))):
            self.verify_one(files[i][0:6], dscore)

        f = open("%s\\hly_count_res_max_4_group_by_date.json" % sys.path[0], "w", encoding="utf-8")
        f.write(json.dumps(self.res, ensure_ascii=False))
        f.close()
        
    def find_EST(self):
        small = ''
        big = ''
        files = os.listdir(self.with_my_result)
        for i in tqdm(range(len(files))):
            try:
                df = pd.read_csv("%s%s" % (self.with_my_result, files[i]), encoding="gbk")
            except:
                print("ERROR")
                continue
            for index,row in df.iterrows():
                if row['sum_20'] == 35 or row['sum_20'] == -33:
                    print(files[i], row['日期'])

if __name__ == "__main__":
    v = Verify()
    # v.verify_one('000001')
    # v.verify_all(dscore=4)
    v.find_EST()
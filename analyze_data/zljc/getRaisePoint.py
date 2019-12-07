import sys
import json
import pandas as pd
from collections import deque
import copy
import numpy as np
import os
from tqdm import tqdm

class ZljcRaisePoint(object):

    def __init__(self, judge_days=3, limit_a=[1], after_days=[3,4,5,6,7]):
        const_path = sys.path[0].replace("\\analyze_data\\zljc", "")
        f = open(const_path + "\\const.json", "r", encoding="utf8")
        self.consts = json.loads(f.read())

        self.zljc_path = self.consts['path']['result']['zljc']
        self.judge_days = judge_days        # 计算回归拟合的天数
        self.res = {}
        self.limit_a = limit_a
        self.after_days = after_days
        self.k_arr = []

    def one(self, code):
        try:
            df = pd.read_csv("%s%s.csv" %(self.zljc_path, code) , encoding="gbk")
        except:
            print("ERROR OPEN %s" % code)
            return
        jcs = deque([])
        jcm = deque([])
        jcl = deque([])
        self.k_arr = []

        for index,row in df[::-1].iterrows():
            if row['日期'] < '2014-01-01':continue
            jcs.append(row["JCS"])
            jcm.append(row["JCM"])
            jcl.append(row["JCL"])

            if (len(jcs) < self.judge_days):
                continue
            # 1. 最后一天的 `JCS > JCM and JCS > JCL`
            if (jcs[-1] < jcm[-1] or jcs[-1] < jcl[-1]):
                jcs.popleft()
                jcm.popleft()
                jcl.popleft()
                continue
            if (jcs[-1]-max(jcm[-1], jcl[-1])) < 2 * abs(jcm[-1] - jcl[-1]):
                jcs.popleft()
                jcm.popleft()
                jcl.popleft()
                continue
            # 2. 前一日之前的所有 `JCS` 必须在 `JCM` 或 `JCL` 下方 ********
            # 2. 前一日之前的所有 `JCS` 不得远大于 `JCM` 或 `JCL`
            flag = True
            for i in range(self.judge_days - 2):
                # if jcs[i] > jcm[i] or jcs[i] > jcl[i]:
                if (jcs[i]-max(jcm[i], jcl[i])) > 2 * abs(jcm[i] - jcl[i]):
                    flag = False
            if not flag:
                jcs.popleft()
                jcm.popleft()
                jcl.popleft()
                continue
            # 3. 第二日趋势为上升
            for a in self.limit_a:
                # 检查是否满足条件
                if self.is_raise(jcs, a):
                    # 验证 n 天后是否价格上涨
                    for day in self.after_days:
                        if index - day < 0: continue
                        # print(code, ":", row['日期'])
                        self.update_res(a,day,code, row['日期'], df.loc[index-day, "收盘价"] > row['收盘价'])
        # print(self.res)
        # print(self.res)

    def all(self):
        filelist = os.listdir(self.zljc_path)
        for i in tqdm(range(len(filelist))):
            self.one(filelist[i][0:6])
        f = open("%s\\zljc_day_a.json" % sys.path[0], "w", encoding="utf-8")
        f.write(json.dumps(self.res, ensure_ascii=False))
        f.close()

    def is_raise(self, arr, limit_a, type=1):
        if type == 2:
            x = np.array(list(range(len(arr))))
            y = np.array(arr)
            line = np.polyfit(x,y,deg=2)
            return (line[0] > 0 and line[0] >= limit_a) and (-1 * line[1] / (2*line[0]) <= 0)
        if type == 1:
            x = np.array(list(range(len(arr))))
            y = np.array(arr)
            line = np.polyfit(x, y, deg=1)
            self.k_arr.append(line[0])
            if len(self.k_arr) < 2: return False
            return self.k_arr[-1]>0 and self.k_arr[-1] / self.k_arr[-2] > limit_a

    def update_res(self, a, day, code, date, flag):
        if code not in self.res.keys():
            self.res[code] = {}
        if a not in self.res[code].keys():
            self.res[code][a] = {}
        if day not in self.res[code][a].keys():
            self.res[code][a][day] = {}
        if "yes" not in self.res[code][a][day].keys():
            self.res[code][a][day]['yes'] = 0
        if "no" not in self.res[code][a][day].keys():
            self.res[code][a][day]['no'] = 0
        if "dates_yes" not in self.res[code][a][day].keys():
            self.res[code][a][day]['dates_yes'] = []
        if "dates_no" not in self.res[code][a][day].keys():
            self.res[code][a][day]['dates_no'] = []
        if flag:
            self.res[code][a][day]['dates_yes'].append(date)
            self.res[code][a][day]['yes'] += 1
        else:
            self.res[code][a][day]['dates_no'].append(date)
            self.res[code][a][day]['no'] += 1

    def count(self):
        path = sys.path[0]
        f = open("%s\\zljc_day_a.json" % (sys.path[0]), "r", encoding="utf8")
        res = json.loads(f.read())
        count = {}
        for code in res:
            for a in res[code]:
                if not a in count.keys():
                    count[a] = {}
                for day in res[code][a]:
                    if not day in count[a].keys():
                        count[a][day] = {"yes": 0, "no": 0}
                    count[a][day]["yes"] += res[code][a][day]["yes"]
                    count[a][day]["no"] += res[code][a][day]["no"]
        f = open("%s\\zljc_day_a_count.json" % sys.path[0], "w", encoding="utf-8")
        f.write(json.dumps(count, ensure_ascii=False))
        f.close()
            

if __name__ == "__main__":
    # limit_a = [0.010, 0.0125, 0.015, 0.0175, 0.020]
    limit_a = [1.5, 1.75, 2]
    after_days = [3,4,5]
    z = ZljcRaisePoint(limit_a=limit_a, after_days=after_days)
    z.all()
    # z.count()
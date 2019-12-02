import sys
import json
import pandas as pd
import time
import os

from tqdm import tqdm
from functools import reduce
from collections import deque

class HlyScore(object):

    def __init__(self, serial_day_arr=[7], expectation=[5,10,15,20]):
        const_path = sys.path[0].replace("\\analyze_data", "")
        f = open(const_path + "\\const.json", "r", encoding="utf8")
        self.consts = json.loads(f.read())
        self.dayline_file_prefix = self.consts['day_line_file_prefix']['netease_clean']
        self.with_my_result = self.consts['path']['result']['hly']

        self.serial_day_arr = serial_day_arr    # 连续计算的天数
        self.expectation = expectation          # ma 数组
        self.res_matrix = {}
        self.res_matrix_reduce = {}

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
                sum_arr[day].append(row['hly_score'])
                if len(sum_arr[day]) < int(day):
                    df.loc[index,colmun_name % day] = 0
                else:
                    df.loc[index,colmun_name % day] = reduce(lambda x,y:x+y,sum_arr[day])
                    sum_arr[day].popleft()
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

    def analyze_one(self, code):
        try:
            df = pd.read_csv("%s%s.csv" % (self.with_my_result, code), encoding="gbk", error_bad_lines=False)
        except:
            print("ERROR WHILE OPENING %s.csv" % code)
        colmun_name = "MA_%s"
        df = df[::-1]
        ma_arr = {}
        for sum in self.expectation:
            df[colmun_name % sum] = ""
            ma_arr[sum] = deque([])

        for index,row in df.iterrows():
            for ma in ma_arr:
                ma_arr[ma].append(row['收盘价'])
                if len(ma_arr[ma]) < int(ma):
                    df.loc[index,colmun_name % ma] = 0
                else:
                    df.loc[index,colmun_name % ma] = self.get_ma(ma_arr[ma])
                    ma_arr[ma].popleft()
        df[::-1].to_csv("%s%s.csv" % (self.with_my_result, code), encoding="gbk",index=None)

    def analyze_all(self):
        time_start = time.time() 
        file_list = os.listdir(self.dayline_file_prefix)
        file_count = len(file_list)
        for i in tqdm(range(file_count)):
            file = file_list[i]
            code = file[0:6]
            self.analyze_one(code)
        time_end = time.time()
        time_c= time_end - time_start
        print('time cost: %s Seconds' % time_c)

    def get_ma(self, deq):
        res = 0
        for i in deq:
            res += i
        return res / len(deq)

    def transform_js(self):
        codelist = os.listdir(self.with_my_result)
        for i in tqdm(range(len(codelist))):
            file = codelist[i]
            f = open( "%sjs\\%s.js" % (self.with_my_result, file[0:6]),"w", encoding="utf8")
            f.write('''module.exports = [
                ''')
            try:
                df = pd.read_csv(self.with_my_result + file, encoding="gbk",  error_bad_lines=False, index_col=0)
            except:
                print("ERROR OPENING %s"%file)
            for index,row in df.iterrows():
                f.write('''%s,
                '''% row.to_dict())
            f.write(''']''')
            f.close()
                
    def count_one(self, code):
        try:
            df = pd.read_csv("%s%s.csv" % (self.with_my_result, code), encoding="gbk", error_bad_lines=False)
        except:
            print("ERROR OPENING %s.csv " % code)
            return 
        # 1. 读取 表头
        sum_arr = []
        ma_arr = []
        for col in df.columns:
            if col[0:3] == "sum": sum_arr.append(col)
            elif col[0:2] == "MA": ma_arr.append(col)
        for index,row in df[::-1].iterrows():
            # 2. 判断改天的每个打分，对应每个展望值是否呈上升趋势，True，更新矩阵
            # 2.1 遍历打分
            for daysum in sum_arr:
                # 2.2 判断改日打分是否存在
                # !!!!!!!!!!!!!!!!!!!!!!!!
                # 这里在计算时默认天数不足为 0 ，所以打分一定存在，不作判断，可能会影响结果

                # 2.3 遍历 MA
                for ma in ma_arr:
                    # 2.4 判断 ma 日后的 ma 值是否大于当日的 ma
                    # 2.4.1 判断 ma 日后的数据是否还没有
                    if index - int(ma[3:]) < 0:
                        continue
                    if df.loc[index-int(ma[3:]), ma] > row[ma]:
                        self.res_plus_plus(daysum, ma)
                    else:
                        self.res_reduce_reduce(daysum, ma)

    # 统一处理累加
    def res_plus_plus(self, sum_key, ma_key, score_key):
        score_key = "_%s" % score_key
        if not sum_key in self.res_matrix.keys():
            self.res_matrix[sum_key] = {}
        if not ma_key in self.res_matrix[sum_key].keys():
            self.res_matrix[sum_key][ma_key] = {}
        if not score_key in self.res_matrix[sum_key][ma_key]:
            self.res_matrix[sum_key][ma_key][score_key] = 0
        self.res_matrix[sum_key][ma_key][score_key] += 1

    def res_reduce_reduce(self, sum_key, ma_key, score_key):
        score_key = "_%s" % score_key
        if not sum_key in self.res_matrix_reduce.keys():
            self.res_matrix_reduce[sum_key] = {}
        if not ma_key in self.res_matrix_reduce[sum_key].keys():
            self.res_matrix_reduce[sum_key][ma_key] = {}
        if not score_key in self.res_matrix_reduce[sum_key][ma_key]:
            self.res_matrix_reduce[sum_key][ma_key][score_key] = 0
        self.res_matrix_reduce[sum_key][ma_key][score_key] += 1

    def count(self):
        time_start = time.time() 
        file_list = os.listdir(self.dayline_file_prefix)
        file_count = len(file_list)
        for i in tqdm(range(file_count)):
            file = file_list[i]
            code = file[0:6]
            self.count_one(file[0:6])
        time_end = time.time()
        time_c= time_end - time_start
        print('time cost: %s Seconds' % time_c)
        print(self.res_matrix)
        print(self.res_matrix_reduce)
        f = open("%s\\hly_count_res_plus.json" % sys.path[0], "w", encoding="utf-8")
        f.write(json.dumps(self.res_matrix, ensure_ascii=False))
        f.close()

        f = open("%s\\hly_count_res_reduce.json" % sys.path[0], "w", encoding="utf-8")
        f.write(json.dumps(self.res_matrix_reduce, ensure_ascii=False))
        f.close()

    # 将所有操作集中到一起，减少 IO
    def do_all_job_one(self, code):
        # 1. 打开文件
        try:
            df = pd.read_csv("%s%s.csv" % (self.dayline_file_prefix, code), encoding="gbk",  error_bad_lines=False, index_col=0)
        except:
            print("ERROR OPENING %s.csv" % code)
            return
        # 2. 计算打分
        column_name = 'hly_score'
        df = df[::-1]
        df[column_name] = ""
        last_row = pd.Series([])
        for index,row in df.iterrows():
            if last_row.empty: score = 0
            else: score = self.get_score(last_row,row)
            df.loc[index, column_name] = score
            last_row = row
        
        # 3. 计算加分和, 同时计算 MA
        column_name_sum = "sum_%s"
        column_name_ma = "ma_%s"
        
        sum_arr = {}    # 用来保存每个天数队列
        ma_arr = {}

        # 3.1 遍历所有天数和，新建列， 置为空白
        for day_sum in self.serial_day_arr:
            df[column_name_sum % day_sum] = ""
            sum_arr[day_sum] = deque([])
        for sum_ma in self.expectation:
            df[column_name_ma % sum_ma] = ""
            ma_arr[sum_ma] = deque([])


        for index,row in df.iterrows():
            # 3.2 对每个 "和" 的天进行计算
            for day in sum_arr:
                sum_arr[day].append(row['hly_score'])
                if len(sum_arr[day]) < int(day):
                    df.loc[index,column_name_sum % day] = 0
                else:
                    df.loc[index,column_name_sum % day] = reduce(lambda x,y:x+y,sum_arr[day])
                    sum_arr[day].popleft()

            # 3.3 对 每个 MA 的天进行计算
            for ma in ma_arr:
                ma_arr[ma].append(row["收盘价"])
                if len(ma_arr[ma]) < int(ma):
                    df.loc[index, column_name_ma % ma] = 0
                else:
                    df.loc[index,column_name_ma % ma] = self.get_ma(ma_arr[ma])
                    ma_arr[ma].popleft()
        
        # 4. 进行统计

        # 4.1 读取表头
        sum_arr = []
        ma_arr = []
        for col in df.columns:
            if col[0:3] == "sum": sum_arr.append(col)
            elif col[0:2] == "ma": ma_arr.append(col)
        # print(sum_arr)
        # print(ma_arr)
        for index, row in df.iterrows():
            for daysum in sum_arr:
                for ma in ma_arr:
                    # 4.2 判断 ma 日后的 ma 值是否大于当日的 ma
                    # 4.2.1 判断 ma 日后的数据是否还没有
                    if (index-int(ma[3:])) < 0:
                        continue
                    if df.loc[index-int(ma[3:]), ma] > row[ma]:
                        self.res_plus_plus(daysum, ma, row[daysum])
                    else:
                        self.res_reduce_reduce(daysum, ma, row[daysum])
        
        # 5. 全部处理完毕，保存
        # f = open("%s\\tmp\\%s.json" % (sys.path[0],code), "w", encoding="utf-8")
        # f.write(json.dumps(self.res_matrix, ensure_ascii=False))
        # f.close()
        # print(self.res_matrix)
        # print(self.res_matrix_reduce)
        df[::-1].to_csv("%s%s.csv"%(self.with_my_result, code),encoding="gbk",index=None)

    def yes_run_me(self):
        time_start = time.time() 
        file_list = os.listdir(self.dayline_file_prefix)
        file_count = len(file_list)
        for i in tqdm(range(file_count)):
            file = file_list[i]
            code = file[0:6]
            self.do_all_job_one(file[0:6])
        time_end = time.time()
        time_c= time_end - time_start
        print('time cost: %s Seconds' % time_c)
        print(self.res_matrix)
        print(self.res_matrix_reduce)
        f = open("%s\\hly_count_res_plus.json" % sys.path[0], "w", encoding="utf-8")
        f.write(json.dumps(self.res_matrix, ensure_ascii=False))
        f.close()

        f = open("%s\\hly_count_res_reduce.json" % sys.path[0], "w", encoding="utf-8")
        f.write(json.dumps(self.res_matrix_reduce, ensure_ascii=False))
        f.close()

    def run_by_thread(self, thread_num):
        time_start = time.time() 
        file_list = os.listdir(self.dayline_file_prefix)
        file_count = len(file_list)
        offset = file_count / thread_num
        offset = math.ceil(offset)
        threads = []
        for i in range(thread_num):
            start = i * offset
            end = (i+1) * offset if (i+1) * offset < file_count else -1
            thread = threading.Thread(target=self.do_block, args=(start, end))
            threads.append(thread)
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join()
        time_end = time.time()
        time_c= time_end - time_start
        print('time cost: %s Seconds' % time_c)
        print(self.res_matrix)
        print(self.res_matrix_reduce)
        f = open("%s\\hly_count_res_plus.json" % sys.path[0], "w", encoding="utf-8")
        f.write(json.dumps(self.res_matrix, ensure_ascii=False))
        f.close()

        f = open("%s\\hly_count_res_reduce.json" % sys.path[0], "w", encoding="utf-8")
        f.write(json.dumps(self.res_matrix_reduce, ensure_ascii=False))
        f.close()

    def do_block(self, start, end):
        file_list = os.listdir(self.dayline_file_prefix)
        file_list = file_list[start:end]
        for index in tqdm(range(len(file_list))):
            code = file_list[index]
            code = code[0:6]
            self.do_all_job_one(code)

if __name__ == "__main__":
    # serial_day_arr = [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    # expectation = [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    expectation = [5,10,15,20,30]
    serial_day_arr = [6,7,8,9,10]
    hly = HlyScore(serial_day_arr=serial_day_arr,expectation=expectation)
    # hly.calculate_score_all()
    # # hly.calculate_sum_one('000002')
    # hly.calculate_sum_all()
    # hly.analyze_all()
    # hly.transform_js()
    # hly.count()
    hly.yes_run_me()
    # hly.run_by_thread(8)

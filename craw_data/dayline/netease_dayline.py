import sys
import json

from download import download

class NeteaseDayline(object):

    def __init__(self, end_date='99999999', thread_num=1, timeout=10):
        
        const_path = sys.path[0].replace("\\craw_data\\dayline", "")
        # print(const_path)
        f = open(const_path + "\\const.json", "r", encoding='utf8')
        consts = json.loads(f.read())

        self.stock_list_file = consts['stock_list_file']          # 全部股票信息的csv文件
        self.save_path_prefix = consts['day_line_file_prefix']    # 日线存储文件夹目录
        self.end_date = end_date                                  # 截止日期
        self.thread_num = thread_num                              # 线程数
        self.timeout = timeout                                    # 线程超时

        self.downloader = download.Downloader()                   # 下载器
        self.downloader.init_ip_pool()                            # 初始化 ip 池
    
    # 控制器入口
    def entrance(self):
        try:
            df = pd.read_csv(self.stock_list_file, encoding="gbk", error_bad_lines=False)
        except:
            print("ERROR Opening File: %s" % self.stock_list_file)
            return False
        
        codes = []
        for index, row in df.iterrows():
            codes.append(row['股票代码'][1:])       # 字符串第一位为 `（ 增强 csv 文件可读性 ）
        self.craw_by_threads(codes)
        print("\n\n\n\nALL THREADS FINISHED")
        while True:
            if self.is_complete(codes): break
    
    # 多线程抓取
    def craw_by_threads(self, codes):
        all_count = len(codes)
        offset = math.ceil(all_count / thread_num)
        threads = []
        for i in range(self.thread_num):
            start = i * offset
            end = (i+1) * offset if (i+1)*offset < all_count else all_count
            thread = threading.Thread(target=self.craw_block, args=(start, end, codes, i))
            threads.append(thread)
        for t in threads:
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join(timeout=self.timeout)

    # 抓取 codes 块
    def craw_block(self, start, end, codes, thread_id):
        time_start = time.perf_counter()
        block = codes[start:end] if end > 0 else codes[start:]
        # 记录日志
        log_file = "log\\netease_dayline\\thread_%s_%s.txt" % (thread_id, int(time.time()))
        try:
            f = open(log_file, "w")
        except:
            print("ERROR OPENING FILE: %s" % log_file)
        for i in tqdm(range(len(block))):
            code = block[i]
            status = "线程%s: %s下载中 [%s / %s] [%s / %s]" % (thread_id, code, i+1, len(block), time.perf_counter(), time_start)
            f.write(status + "\n")
            try:
                # 进行下载
                filepath = self.save_path_prefix + code + ".csv"
                url = self.handle_netease_url(code)
                self.downloader.download_netease_csv(url=url, filepath=filepath)
            except:
                error = "线程 %s 下载 %s 时出现错误" % (thread_id, code)
                f.write(error + "\n")
                continue

    # 处理网易财经日线 下载的 url
    def handle_netease_url(self, code):
        # 处理代码前缀
        netease_prefix = ""
        if str(code)[0] == "0" or str(code)[0] == "3":
            netease_prefix = "1"
        elif str(code)[0] == "6":
            netease_prefix = "0"
        code = str(netease_prefix) + str(code)
        return 'http://quotes.money.163.com/service/chddata.html?code=%s&end=%s&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP' % (code, self.end_date)
    
    # 校验是否全部下载完毕， 下载未下载的
    def is_complete(self, codes):
        print("\n正在校验文件是否完整")
        filelist = os.listdir(self.save_path_prefix)
        print("总共应下载 %s 个文件， 实际下载 %s 个" % (len(codes), len(filelist)))
        if len(filelist) == len(codes): return True
        downloaded = []
        for name in filelist:
            downloaded.append(name[0:6])
        need_to_download = []
        for code in codes:
            if code not in downloaded:
                need_to_download.append(code)
        self.thread_num = 4
        self.craw_by_threads(need_to_download)
        return False

if __name__ == "__main__":
    
    # end_date = "20190616"                                          # 截至日期
    thread_num = 16                                                  # 线程数
    timeout = 10                                                     # 线程超时

    netease_dayline = NeteaseDayline(
        thread_num=thread_num, 
        timeout=timeout
    )
    # netease_dayline.entrance()
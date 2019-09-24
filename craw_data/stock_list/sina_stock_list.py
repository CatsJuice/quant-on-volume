import sys
sys.path.append(sys.path[0].replace('stock_list', '') + 'dayline')
from download import download
import json
from tqdm import tqdm
import ast

uri = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=%s&num=40&sort=amount&asc=0&node=hs_a&symbol=&_s_r_a=auto"

class SinaStockList(object):

    def __init__(self):
        const_path = sys.path[0].replace("\\craw_data\\stock_list", "")
        f = open(const_path + '\\const.json', 'r', encoding='utf8')
        self.consts = json.loads(f.read())
        
        self.downloader = download.Downloader()
        self.downloader.init_zhilian_ip()
        # self.downloader.init_ip_pool()

        self.arr = []

    def get_stock_list(self, max_page=100):
        for i in tqdm(range(max_page)):
            res = self.downloader.zhilian_ip_proxy_get(uri % i).decode("gbk","ignore")
            if res == "null":
                continue
            res = json.loads(self.json_format(res))
            # print(res)
            self.arr.extend(res)
        with open(self.consts['path']['stock_list']['sina'] + "\\stock_list.json", "w", encoding="utf-8") as f:
            json.dump(self.arr, f, ensure_ascii=False)

    def json_format(self, str):
        import re
        str = re.sub(u'{([^{:]*):', u'{"\\1":', str)
        str = re.sub(u',([^,:{]*):', u',"\\1":', str)
        str = str.replace(' ', '')
        return str

if __name__ == "__main__":
    sina_stock_list = SinaStockList()
    sina_stock_list.get_stock_list()
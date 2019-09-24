import json
import sys
import requests
from bs4 import BeautifulSoup
import random
import time

class IpManage(object):

    def __init__(self, max_ip_num):
        self.ip_pool = []   # ip池数组

        const_path = sys.path[0].split("quant-on-volume")[0] + "quant-on-volume"
        f = open(const_path + '\\const.json', "r", encoding="utf8")
        consts = json.loads(f.read())
        self.check_url = consts['check_url1']        # 校验ip是否可用的 url
        self.type = consts['type']                  # https / http
        self.pages = []                             # 已爬取的 page 数组
        self.max_ip_num = max_ip_num                # 要爬取的 ip 数量上限

    # 抓取单页的ip
    def craw_ips_by_page(self, page):
        url = "https://www.xicidaili.com/nn/%s" % page
        html_content = self.requests_get(url, 'html')
        
        if html_content == "0":
            print("获取ip池失败， 请检查网络设置， 并确认本机ip没有被封禁")
            return
        soup = BeautifulSoup(html_content, 'html.parser')
        all_trs = soup.find("table", id="ip_list").find_all('tr')
        for tr in all_trs[1:]:
            tds = tr.find_all('td')
            ip = {
                'ip': tds[1].get_text(),
                'port': tds[2].get_text(),
                'type': tds[5].get_text()
            }
            # 检查ip是否可用
            if self.check_ip(ip):
                self.ip_pool.append(ip)
            if len(self.ip_pool) >= self.max_ip_num:
                break
    
    # 获取 IP 池
    def craw_ips(self):
        page = self.get_random_page()
        self.pages.append(page)
        print("当前爬取的ip页码为： ", page)
        self.craw_ips_by_page(page)
        
        # 判断 ip 数量是否已足够
        if len(self.ip_pool) < self.max_ip_num:
            self.craw_ips()
        else:
            with open(sys.path[0] + "\\ip_pool.json", "w", encoding="utf-8") as f:
                json.dump(self.ip_pool, f)
            print("共抓取 %s 条ip" % len(self.ip_pool))
        
    # 检查代理ip是否可用
    def check_ip(self, ip):
        proxy_temp = {
            "http": "http://%s:%s" % (ip['ip'], ip['port']),
            "https": "http://%s:%s" % (ip['ip'], ip['port'])
        }
        show_info = self.check_url + "---" + "http://%s:%s  [%s]" % (ip['ip'], ip['port'], time.perf_counter())
        try:
            # print(show_info)
            res = requests.get(self.check_url, timeout=1, proxies=proxy_temp)
            if res.status_code == 200:
                print(show_info, ":SUCCESS")
                return True
            else:
                print(show_info, ":FAIL")
                return False
        except:
            print(show_info, ":FAIL")
            return False

    # get 请求
    def requests_get(self, url, type, data=None):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers, data=data)
        if response.status_code == 200:
            if type == "img":
                # 获取图片
                return response.content
            if type == "html":
                html = response.content
                html_content = html.decode("utf-8", "ignore")
                return html_content 
            if type == "text":
                return response.text
        else:
            print("Request Falied For Code: %s" % response.status_code)
            return "0"

    # 生成随机页码
    def get_random_page(self):
        max_page = 3000
        page = 0
        while True:
            page = random.randint(0, max_page)
            if page not in self.pages:
                break
        return page

# if __name__ == "__main__":
#     ip_manage = IpManage(10)
#     ip_manage.craw_ips();

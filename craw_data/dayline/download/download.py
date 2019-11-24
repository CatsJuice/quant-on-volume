import os
import sys
import time
import json
import requests
import random
import urllib
import http.client
import csv
from bs4 import BeautifulSoup
try:
    import ip as ipmanage
except:
    from download import ip as ipmanage

class Downloader(object):

    def __init__(self):
        self.ip_pool = []
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }

    # 初始化IP池
    def init_ip_pool(self, ip_num=100):
        try:
            t = os.path.getmtime(sys.path[0] + "\\ip_pool.json")
            flag = True
        except:
            flag = False
        if flag and time.time() - t < 3600:      # ip池未过期, 调用本地缓存
            f = open(sys.path[0] + "\\ip_pool.json", "r", encoding="utf8")
            self.ip_pool = json.loads(f.read())
        else:
            ip_manage = ipmanage.IpManage(max_ip_num=ip_num)
            ip_manage.craw_ips()
            self.ip_pool = ip_manage.ip_pool

    # get 请求
    def requests_get(self, url, type, data=None):
        response = requests.get(url=url, headers=self.headers, data=data)
        if response.status_code == 200:
            # request successfully
            if type == "img":
                # 获取图片
                return response.content
            if type == "html":
                html = response.content
                # html_content = str(html,'utf-8')
                html_content = html.decode("utf-8","ignore")
                return html_content
            if type == "text":
                return response.text
            if type == "json":
                return response.content
        else:
            print("Request Falied For Code: %s" % response.status_code)
            return "0"

    # post 请求
    def requests_post(self, url, type, data=None):
        response = requests.post(url=url, headers=self.headers, data=data)
        if response.status_code == 200:
            # request successfully
            if type == "img":
                # 获取图片
                return response.content
            if type == "html":
                html = response.content
                # html_content = str(html,'utf-8')
                html_content = html.decode("utf-8","ignore")
                return html_content
            if type == "text":
                return response.text
        else:
            print("Request Falied For Code: %s" % response.status_code)

    def download_netease_csv(self, url, filepath):
        # response = requests.get(url=url)
        # with open(filepath, "wb", encoding="gbk") as f:
        #     f.write(response.content)
        http.client.HTTPConnection._http_vsn = 10
        http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
        urllib.request.urlretrieve(url, filepath)


    # 通过代理发起 get 请求
    def proxy_get(self, url, type, data=None):
        # try:
            ip = self.ip_pool[random.randint(0, len(self.ip_pool)-1)]
            proxy = {
                "http": "http://%s:%s" % (ip['ip'], ip['port'])
            }
            print(proxy)
            response = requests.get(url, proxies=proxy, headers=self.headers, data=data)
            # response = requests.get(url=url, headers=self.headers, data=data)
            if response.status_code == 200:
                # request successfully
                if type == "img":
                    # 获取图片
                    return response.content
                if type == "html":
                    html = response.content
                    # html_content = str(html,'utf-8')
                    html_content = html.decode("utf-8","ignore")
                    return html_content
                if type == "text":
                    return response.text
            else:
                print("Request Falied For Code: %s" % response.status_code)
                return "0"
        # except:
            # return "0"

    # 通过 代理ip平台的ip获取get请求
    def zhilian_ip_proxy_get(self, url):
        zhilian_ip_json_path = sys.path[0].split("quant-on-volume")[0] + "quant-on-volume\\zhilian_ip.json"
        f = open(zhilian_ip_json_path, 'r', encoding="utf-8")
        ips = json.loads(f.read())
        while True:
            ip = ips[random.randint(0, len(ips)-1)]     # 随机 ip
            try:
                proxy = {
                    "http": "http://%s:%s" % (ip['IP'], ip['Port']),
                    "https": "http://%s:%s" % (ip['IP'], ip['Port'])
                }
                response = requests.get(url, proxies=proxy, headers=self.headers, timeout=1)
                if response.status_code == 200:
                    return response.content
                elif response.status_code == 503:
                    self.init_zhilian_ip()
                else:
                    print("http://%s:%s" % (ip['IP'], ip['Port']), ":FAILED-1")
                    continue
            except:
                print("http://%s:%s" % (ip['IP'], ip['Port']), ":FAILED-2")

    # 初始化 智联 ip
    def init_zhilian_ip(self):
        # url = input("输入api:\n")
        url = "http://t.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=1&fa=0&fetch_key=&qty=100&time=1&pro=&city=&port=1&format=json&ss=5&css=&dt=1&specialTxt=3&specialJson=&usertype=16"
        response = requests.get(url)
        ips = json.loads(response.content)['data']
        zhilian_ip_json_path = sys.path[0].split("quant-on-volume")[0] + "quant-on-volume\\zhilian_ip.json"
        with open(zhilian_ip_json_path, "w") as f:
            json.dump(ips, f)
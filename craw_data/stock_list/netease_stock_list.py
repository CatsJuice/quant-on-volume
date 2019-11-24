import urllib
import json
import csv
from tqdm import tqdm

# 下载器
class Downloader(object):
    def __init__(self, url):
        self.url = url

    def download(self):
        html_content = urllib.request.urlopen(self.url).read()
        html_content = html_content.decode("utf-8")
        return html_content

# 调度器
class Controller(object):

    def __init__(self):
        self.downloader = None
        self.parser = None
        self.saver = None

    def get_data(self):
        url = "http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page=0&query=STYPE%3AEQA&fields=NO%2CSYMBOL%2CNAME%2CPRICE%2CPERCENT%2CUPDOWN%2CFIVE_MINUTE%2COPEN%2CYESTCLOSE%2CHIGH%2CLOW%2CVOLUME%2CTURNOVER%2CHS%2CLB%2CWB%2CZF%2CPE%2CMCAP%2CTCAP%2CMFSUM%2CMFRATIO.MFRATIO2%2CMFRATIO.MFRATIO10%2CSNAME%2CCODE%2CANNOUNMT%2CUVSNEWS&sort=PERCENT&order=desc&count=3607&type=query"
        html_content = urllib.request.urlopen(url).read()
        # 这时候解码可能导致json解析错误!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # html_content = html_content.decode("unicode_escape")
        # 当数量大于2995会报错， json解析失败， 原因是编号为2996的股票， 在公告中嵌套了引号导致json解析失败
        data = json.loads(html_content)

        self.saver = Saver(data=data)
        self.saver.save()

class Saver(object):

    def __init__(self, data):
        self.data = data
        const_path = sys.path[0].replace("\\craw_data\\stock_list", "")
        f = open(const_path + '\\const.json', 'r', encoding='utf8')
        self.consts = json.loads(f.read())
        self.file_path = self.consts['path']['stock_list']['netease'] + "\\stock_list.json"      # 存放目录

    def save(self):
        # 新建文件, 写入文件头
        file_header = ["代码", "名称", '流通市值', '每股收益', '总市值']
        csv_file = open(self.file_path, 'w', newline='')
        writer = csv.writer(csv_file)
        writer.writerow(file_header)

        list = self.data['list']
        sum = len(list)
        for i in tqdm(range(0, sum)):
            item = list[i]

            # 处理股票代码， 去掉网易财经的0/1前缀， 并使其在Excel中显示正常（加`）
            code = str(item['CODE'])
            code = code[1:7] if len(code) == 7 else code[:]
            code = "`" + code

            row = [code, item['NAME'], item['MCAP'], item['MFSUM'], item['TCAP']]
            csv_file = open(self.file_path, 'a', newline='')      # 追加
            writer = csv.writer(csv_file)
            writer.writerow(row)


if __name__ == '__main__':
    controller = Controller()
    controller.get_data()
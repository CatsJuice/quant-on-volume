基于成交量的股票数据分析系统

# 1. 数据获取

## 1.1. 实验环境搭建

系统及使用的语言：

> Windows 10 专业版 1903 操作系统版本： 18362.356
> 
> Python 3.7.3 64-bit

需要额外安装的库：

> virtualenv-16.6.0： `pip install virtualenv`

> requests-2.22.0： `pip install requests`
>
> 所依赖的模块：`urllib3` 在安装 `requests` 时会自动安装

> BeautifulSoup4-4.8.0：`pip install BeautifulSoup4`

> pandas: `pip install pandas`
>
> 所依赖的模块：`pytz` ,`numpy`, `python-dateutil`, `six`, 在安装 `requests` 时会自动安装

> tqdm-4.36.1: `pip install tqdm`

## 1.2. 抓取数据

### 1.2.1. 新浪财经

#### 1.2.1.1. 抓取所有股票代码

进入新浪财经官网进行查找， 可以在

```bash
行情中心首页 > 沪深股市 > 排行 > A股成交额
```

找到成交额的排行耪， 这里可以获取到所有沪深A股的股票代码; 链接地址如下：

> [http://vip.stock.finance.sina.com.cn/mkt/#stock_hs_amount](http://vip.stock.finance.sina.com.cn/mkt/#stock_hs_amount)

**分析页面**

首先可以看到请求的 url 中有 `#` 字符，使用了 `hash` 路由, 初步判断页面使用前端框架加打包工具构建， 数据很可能是异步加载的；

尝试跳转下一页， 页面的 `url` 没有发生变化（并未出现page或相应页码等关键字）, 所以通过调试工具（F12打开开发者工具）, 切换到 网络（`Network`）栏， 只查看 `XHR` ( `XMLHttpRequest` ), 此时在跳转页码时， 会通过 `GET` 请求获取数据， 分析请求的 `url` 如下:

```bash
https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=3&num=40&sort=amount&asc=0&node=hs_a&symbol=&_s_r_a=auto
```

在其中最为关键的数据即是 `page` 的值，而其返回的数据格式为喜闻乐见的 `json`，至此抓取的准备工作全部完毕， 可以进行抓取，在抓取的时候需要注意的是预防因并发过高导致本机 `ip` 被封锁， 关于这一点的预防手段在  作详述；

**数据抓取**

在浏览器中直接访问链接可以请求到数据内容， 查看页面编码为 `GBK` ,直接使用 `requests` 模块通过 `GET` 请求页面，初步抓取到数据， 尝试直接使用 `json.loads()` 将字符串转为字典发生错误， 这里对获取的字符串进行分析，其基本格式如下：

```json
[
    {symbol:"sh600519",code:"600519",name:"贵州茅台",trade:"1178.580", ...},
    ...
]
```

关键在于其格式不符合 `json` 的基本格式， 这种格式在 `JavaScript` 中作为对象可以解析， 但对 `json` 来说是不合法的；尝试使用 `eval()` / `ast.literal_eval()` 来替代 `json`, 同样无法直接解析， 所以需要更改思路， 手动更改字符串的格式， 给字典的键添加双引号， 编写正则替换方法如下：

```py
def json_format(self, str):
    import re
    str = re.sub(u'{([^{:]*):', u'{"\\1":', str)
    str = re.sub(u',([^,:{]*):', u',"\\1":', str)
    str = str.replace(' ', '')
    return str
```
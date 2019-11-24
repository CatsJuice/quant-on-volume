
# `pcap` 和 `dpkt` 的安装
 
 首先 `dpkt` 的安装较为简单， 直接使用 `pip install dpkt` 即可
 
 而 `pcap` 的安装相对麻烦，(GitHub: [https://github.com/pynetwork/pypcap](https://github.com/pynetwork/pypcap))具体安装步骤如下：
 - 尝试 `pip install pypcap` 
 - 下载(clone)源代码： [https://github.com/pynetwork/pypcap](https://github.com/pynetwork/pypcap)
 - 执行 `python setup.py install`
 - 如果遇到 `pcap.h not found`, 则需要安装 `Npcap SDK`, 下载地址：[https://nmap.org/npcap/](https://nmap.org/npcap/)
 - 下载后，将 `npcap sdk` 解压，放置在与 `pcap` 同级目录， 如下：
 ```bash
 ├───pypcap-1.2.1
 │   ├───docs
 │   ├───pypcap.egg-info
 │   └───tests
 └───wpdpack
     ├───docs
     ├───...
     └───npcap-sdk-1.04
 ```
 - 然后再执行 `python setup.py install`
 - 如果遇到 `Microsoft Visual C++ 14.0 is required` 则需要安装 C++ 14.0 再进行安装
 - 安装成功后，如果在 `import pcap` 时遇到 `ImportError: DLL load failed` , 执行操作如下：
   - 下载 [`Npcap` 安装程序](https://nmap.org/npcap/dist/npcap-0.9984.exe)
   - 安装时勾选 `WinPcap Compatible Mode`
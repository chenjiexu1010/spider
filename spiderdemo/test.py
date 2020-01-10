# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import time
import requests
import json
from selenium import webdriver

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'MWeibo-Pwa': '1',
    'Referer': 'https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D%E5%A9%9A%E7%BA%B1',
    'X-XSRF-TOKEN': '2b4ca4',
    'Host': 'm.weibo.cn',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'X-Requested-With': 'XMLHttpRequest',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cookie': '_T_WM=70659849320; WEIBOCN_FROM=1110006030; ALF=1580892365; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFOfqD9fkE8ALcVFJfdDIpl5JpX5K-hUgL.FozR1KnReK2NSo-2dJLoIfQLxK-L12qL1KqLxKBLBonLB-2LxK-L1K5L12BLxK-LB-BL1KMLxKBLBo.L1-qLxK-LB.-L1hnLxK.L1-2LB.-LxK-L1K-L122LxKqL1hnL1K2LxK-L12-LB.zt; SCF=AncjsCf7zbAbUzNBAKOizieYzy1LkJJc5eum43dQUuxtrATTSPTWG7w7tKqvAmIsYQJnKSCEaS6FZ3AWlQtoApE.; SUB=_2A25zFor6DeRhGeRG4loZ8S_LzTmIHXVQ-BayrDV6PUJbktANLWXFkW1NTeZINBbp_X_wJXik17ygh-yimqeJDhLt; SUHB=0ebdehCpVN1nm_; SSOLoginState=1578302122; MLOGIN=1; XSRF-TOKEN=292255; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100103type%253D1%26fid%3D100103type%253D1%26uicode%3D10000011'
}

url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%E5%A9%9A%E7%BA%B1&page_type=searchall'
result = requests.get(url=url, headers=headers)
print(result.status_code)
blog_list = result.json()['data']['cards']
for blog in blog_list:
    print(blog)

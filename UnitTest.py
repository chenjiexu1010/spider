# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import requests
import json
from collections import defaultdict
import collections
import logging
from selenium import webdriver

oasis_type_url = 'http://222.185.251.62:22027/api/GetLvZhouData'
headers = {'Content-Type': 'application/json'}
body = {'PhoneCode': '小米手机09'}
re = requests.post(oasis_type_url, headers=headers, data=json.dumps(body))
print(re.content)

# url = 'http://192.168.2.74:5001/comscreenshot/海外婚礼/4459164203837822'
# res = requests.get(url)
# print(res.text)
# print(res.content)
# print(res.text.encode('utf-8'))
# print('--执行结束--')

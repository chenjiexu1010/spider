# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import requests
import json
from collections import defaultdict
import collections
import logging

url = 'http://192.168.2.74:5001/comscreenshot/海外婚礼/4459480341597419'
res = requests.get(url)
print(res.content)
print('--执行结束--')

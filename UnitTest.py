# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import requests
import json
from collections import defaultdict
import collections
from collections import Counter
from collections import deque
from functools import lru_cache
from contextlib import contextmanager
import uiautomator2 as u2

'''
"[{\"id\":2173,\"key\":\"海外婚礼\",\"typecode\":\"JQHOT_0300\"},
  {\"id\":2172,\"key\":\"婚礼布置\",\"typecode\":\"JQHOT_0300\"},
  {\"id\":2171,\"key\":\"婚礼策划\",\"typecode\":\"JQHOT_0300\"},
  {\"id\":2170,\"key\":\"旅拍\",\"typecode\":\"JQHOT_0300\"},
  {\"id\":2169,\"key\":\"婚纱照\",\"typecode\":\"JQHOT_0300\"}]"
'''

code = 'jeqeehot'
headers = {'Content-Type': 'application/json'}
body = {
    'code': code
}

url = 'http://222.185.251.62:22027/api/business/getlvzhoushot'
request = requests.post(url=url, headers=headers, data=json.dumps(code))
print(type(request.text))
dumps_str = json.loads(request.text)
dumps_str2 = json.loads(dumps_str)
for dump in dumps_str2:
    print(dump)

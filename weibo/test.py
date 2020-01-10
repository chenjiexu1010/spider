# -*- coding:utf-8 -*-
# !/usr/bin/Python3

import uiautomator2 as u2
import time
import urllib.request
import requests

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}
com_url = 'http://192.168.2.74:5000/comshot2/海外婚礼/美好回忆。/0'

result = requests.get(url=com_url, headers=header)


# fruits = ['apple', 'banana', 'mango']
# for fruit in fruits:
#     print(fruit.capitalize())

# a_list = [[1, 2], [3, 4], [5, 6]]
# print(list(itertools.chain.from_iterable(a_list)))

# items = [1, 2, 3, 4, 5, 6]
# squared = list(map(lambda x: x * 2, items))
# print(squared)

# a = [(1, 2), (4, 1), (9, 10), (13, -3)]
# a.sort(key=lambda x: x[1])
# print(a)
# s = '婚纱'
# s = ord(s)
# print(s)

# url = 'http://222.185.251.62:22027/api/GetRedBookData'
# # client = Client(url)
# # print(client)
# body = {'PhoneCode': '小米手机01'}
# header = {'Content-Type': 'application/json'}
#
# re = requests.post(url, headers=header, data=json.dumps(body))
# re.encoding = 'utf-8'
# print(re.text)
# print(re.status_code)

# im = array(Image.open('8ce46dde-f9ef-11e9-a3c1-40167eaae4e9.jpg'))
# print(type(im))
# print(im.__array__())

# search_str = '汽车日常小常识'
# d = u2.connect_usb('emulator-5610')
# d.screenshot('home.jpg')

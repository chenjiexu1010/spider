# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import uiautomator2 as u2
import cv2
import json
import requests

'''
    1. 数据库
    2. 
'''

'''
{'bottom': 1002, 'left': 45, 'right': 503, 'top': 888}
'''

d = u2.connect_usb('93d3c879')
d.screenshot('test.png')
# print(d(text='大理婚纱照💭大理旅拍婚纱摄影图片汇总').info)

# 下载图片
# req = requests.get('http://222.185.251.62:8120/7,025d5ee00e1300', stream=True)
# if req.status_code == 200:
#     with open('test.png', 'wb') as f:
#         for chunk in req:
#             f.write(chunk)
img = cv2.imread('test.png')
# 坐标(左上，右下）
cv2.rectangle(img, (45, 888), (503, 1002), (0, 0, 255),
              5)
cv2.imwrite('001_new3.png', img)

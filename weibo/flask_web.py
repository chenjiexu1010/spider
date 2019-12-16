# -*- coding:utf-8 -*-
# !/usr/bin/Python3
from flask import Flask
from spider.weibo.weibo_screenhot import WeiBoScreenShot
import json

# 连接设备 8c5a04d2 usb 链接 可采用wife
device_num1 = '8c5a04d2'
# device_num2 = ''

# 初始化设备程序
m1 = WeiBoScreenShot(device_num1)
# m2 = WeiBoScreenShot(device_num2)

device_dic = {device_num1: m1}
# 端口
host = '192.168.2.74'
# flack
app = Flask(__name__)

is_on = False


@app.route('/hotscreen/<key>/<content>')
def hot_screen(key, content):
    global is_on
    if is_on:
        return '设备忙绿'
    if key == '' or content == '':
        return '参数错误'
    is_on = True
    res = device_dic[device_num1].hot_screen_hot(key, content)
    is_on = False
    if res:
        return json.dumps(res)
    return '截图失败'


@app.route('/realtime/<key>/<content>')
def realtime_screen(key, content):
    global is_on
    if is_on:
        return '设备忙绿'
    if key == '' or content == '':
        return '参数错误'
    is_on = True
    res = device_dic[device_num1].time_screen_hot(key, content)
    is_on = False
    if res:
        return json.dumps(res)
    return '截图失败'


if __name__ == '__main__':
    app.run(host=host, port=5000)

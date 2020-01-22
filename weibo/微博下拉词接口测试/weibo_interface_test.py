# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import requests
import json

# 新增下拉url
add_url = 'http://222.185.251.62:22027/api/weibo/addword'
# 获取任务url
get_task_url = 'http://222.185.251.62:22027/api/weibo/getdropdownword'
# 暂停任务url
stop_task_url = 'http://222.185.251.62:22027/api/weibo/stopdropdowntask'
#  TODO WCF服务正式环境未发 提交任务
submit_task_url = 'http://222.185.251.62:22027/api/weibo/submitdropdowntask'

header = {
    'Content-Type': 'application/json'
}

body = {
    "SearchWord": "牙齿矫正精准客源",
    "IsOnPage": False,
    "CurrentIndex": 0,
    "Message": "",
    "CurrentRank": 0
}
'''
婚礼策划客源引流
体彩吲留找小川
微信弓丨流魔法师

'''

# stop_req = requests.post(add_url, headers=header, data=json.dumps('微信弓丨流魔法师'))
# print(stop_req.content)

# 提交测试
# req = requests.post(submit_task_url, headers=header, data=json.dumps(body))
# con = json.loads(req.content.decode('utf8'))
# print(con)

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

美瞳安利找肉肉美瞳店
零食推荐进口加盟yami
情感挽回吲流MCOCO
推广吲流M魔法师
竞彩吲流M我吧
足彩吲流M小川
代购吲流M魔法师
微信吲流M魔法师

'''
with open('dropdownwords.txt', 'r', encoding='utf8') as r:
    words = r.read().splitlines()
    for word in words:
        stop_req = requests.post(add_url, headers=header, data=json.dumps(word))
# print(stop_req.content)

# 提交测试
# req = requests.post(submit_task_url, headers=header, data=json.dumps(body))
# con = json.loads(req.content.decode('utf8'))
# print(con)

# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import cv2
import json
import time
import requests
import os

pic_name = 'logo.png'

oasis_type_submit_url = 'http://222.185.251.62:22027/api/UpdateLvZhouPicCheck'
xhs_submit_url = 'http://222.185.251.62:22027/api/UpdateRedBookPicCheck'

# 测试url
rb_hot_submit_url = 'http://222.185.251.62:22027/api/redbook/submithotcomment'

# 微博下拉账号提交
weibo_drop_submit = 'http://222.185.251.62:22027/api/PostWeiBoDdaData'


class PicHandle(object):
    def __init__(self):
        self.get_task_url = 'http://222.185.251.62:22027/api/phone/getpichandle'
        # self.get_task_url = 'http://localhost:22027/api/phone/getpichandle'
        self.headers = {'Content-Type': 'application/json'}

    # 获取任务
    def get_task(self):
        while True:
            try:
                # 获取图片处理
                req = requests.post(url=self.get_task_url, headers=self.headers)
                if req.status_code == 200:
                    res = json.loads(req.text)
                    if '任务为空' in res:
                        time.sleep(60 * 1)
                        continue
                    res = json.loads(res)
                    print(res)
                    req = requests.get(res['PicUrl'], stream=True)
                    if req.status_code == 200:
                        with open(pic_name, 'wb') as f:
                            for chunk in req:
                                f.write(chunk)
                    img = cv2.imread(pic_name)
                    #  坐标(左上，右下）
                    cv2.rectangle(img, (res['Left'], res['LeftTop']), (res['Right'], res['RightBottom']), (0, 0, 255),
                                  5)
                    cv2.imwrite('001_new3.png', img)
                    b = PicHandle.pic_to_byte(self, '001_new3.png')
                    body = {
                        'Id': res['LogId'],
                        'TaskId': res['TaskId'],
                        'TypeCode': res['TypeCode'],
                        'PicCheck': json.dumps(b),
                        'Message': '成功',
                    }
                    if res['TypeCode'] == 'JQHOT_0300':  # 绿洲SEO
                        re = requests.post(oasis_type_submit_url, headers=self.headers, data=json.dumps(body))
                        print(re.text)
                    if res['TypeCode'] == 'JQHOT_0200':  # 小红书SEO
                        requests.post(xhs_submit_url, headers=self.headers, data=json.dumps(body))
                    if res['TypeCode'] == 'JQHOT_0202':  # 小红书热评
                        body = {
                            'LogId': res['LogId'],
                            'Pic': json.dumps(b)
                        }
                        requests.post(rb_hot_submit_url, headers=self.headers, data=json.dumps(body))
                    if res['TypeCode'] == 'JQHOT_0106':
                        body = {
                            'LogId': res['LogId'],
                            'PicStr': json.dumps(b)
                        }
                        requests.post(weibo_drop_submit, headers=self.headers, data=json.dumps(body))
                    os.remove(pic_name)
                    os.remove('001_new3.png')
                    print('成功提交一条任务')
                else:
                    print('状态码不为200:%s' % req.status_code)
            except Exception as e:
                print(e)

    def pic_to_byte(self, pic_name):
        b = []
        with open(pic_name, 'rb') as f:
            for i in f.read():
                b.append(i)
        return b


if __name__ == '__main__':
    pic = PicHandle()
    pic.get_task()

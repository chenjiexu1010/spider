# -*- coding:utf-8 -*-
# !/usr/bin/Python3

import uiautomator2 as u2
import time
import uuid
import os
import requests
import json

pic_handle_insert_url = 'http://222.185.251.62:22027/api/phone/pichandle'
pic_change_url = 'http://222.185.251.62:22027/api/phone/getpicurl'


class XhsSearch(object):
    def __init__(self):
        self.d = u2.connect('http://0.0.0.0')
        # self.d = u2.connect_usb('56d78870')
        self.number = 0
        self.d.watcher("ALERT").when(text="取消")
        self.d.watcher("ALERT").when(text="下次再说").click()
        self.get_xhs_url = 'http://222.185.251.62:22027/api/GetRedBookData'
        self.submit_url = 'http://222.185.251.62:22027/api/UpdateRedBookPicCheck'
        self.body = {'PhoneCode': '小米手机11'}
        self.headers = {'Content-Type': 'application/json'}
        self.phonecode = '小米手机11'
        self.typecode = '小红书SEO'
        self.location = {}
        self.update_phone_url = 'http://222.185.251.62:22027/api/phone/updatephoneinfo'
        # self.d.healthcheck()
        print('手机连接成功')
        # 打开app
        XhsSearch.app_start(self)

    def update_phone(self, typecode, logtype, phone_code):
        body = {
            "PhoneCode": phone_code,
            "TypeCode": typecode,
            "Message": "检测手机状态",
            "LogType": logtype
        }
        requests.post(self.update_phone_url, headers=self.headers, data=json.dumps(body))

    # 清楚缓存重新登录
    def app_clear(self):
        pass

    # 启动app
    def app_start(self):
        self.d.screen_on()
        self.d.app_start('com.xingin.xhs', use_monkey=True)
        self.d.app_wait('com.xingin.xhs', front=True, timeout=20)
        is_exist = self.d(text='跳过广告').exists()
        if is_exist:
            self.d(text='跳过广告').click()
        is_exist = self.d(text='同意').exists()
        if is_exist:
            self.d(text='同意').click()
        time.sleep(10)
        is_exist = self.d(text='取消').exists()
        if is_exist:
            self.d(text='取消').click()

    # 关键词截图
    def key_world_search(self, key_world, content):
        set2 = set()
        match_title = False
        match_name = False
        XhsSearch.judge_is_home(self)
        try:
            if self.d(resourceId='com.xingin.xhs:id/adu').exists():
                self.d(resourceId='com.xingin.xhs:id/adu').click()
                time.sleep(2)
                if self.d(className='android.widget.EditText').exists():
                    self.d(className='android.widget.EditText').click()
                    # self.d.set_fastinput_ime(True)
                    self.d(className='android.widget.EditText').send_keys(key_world)
                    # self.d.send_keys(key_world)
                    # self.d.set_fastinput_ime(False)
                    time.sleep(3)
                    if self.d(text='搜索').exists():
                        self.d(text='搜索').click()
                        # 等待响应页面
                        time.sleep(5)
                    else:
                        return ''
                else:
                    return ''
            else:
                return ''
            while True:
                if len(set2) > 50:
                    self.number = 0
                    print('搜索达到上限 50篇笔记')
                    break
                # # 匹配内容
                for title in self.d(resourceId='com.xingin.xhs:id/b3e'):
                    set2.add(title.info['text'])
                    if content in title.info['text']:
                        self.location = {}
                        match_title = True
                        top = title.info['bounds']['top']
                        # 移动笔记到指定位置
                        XhsSearch.move_ele_position(self, top, title.info['text'])
                        time.sleep(5)
                        self.location = self.d(textContains=content).info
                        break
                    # if match_title:
                    #     break
                    # 匹配名称 判断是否匹配到内容
                    # if not match_name:
                    #     for nickname in self.d(resourceId='com.xingin.xhs:id/b3g'):
                    #         if name in nickname.info['text']:
                    #             match_name = True
                    #             # top = nickname.info['bounds']['top']
                    #             # 移动笔记到指定位置
                    #             # XhsSearch.move_ele_position(self, top, nickname)
                    #             # time.sleep(2)
                    #             break
                # 找到标题 获取 昵称
                if len(set2) < 10:
                    if match_title or match_name:
                        # TODO 截全图
                        name = str(uuid.uuid1()) + '.png'
                        self.d.screenshot(name)
                        b = XhsSearch.pic_to_byte(self, name)
                        os.remove(name)
                        return b
                        # 下滑
                self.d.swipe_ext('up', scale=0.2)
                time.sleep(2)
        except Exception as e:
            print(e)

    # 移动笔记位置
    def move_ele_position(self, top, text):
        self.d(text=text).gesture(
            (0, top),
            (0, top),
            (0, 1272),
            (0, 1272))

    # 图片转字节
    def pic_to_byte(self, pic_name):
        b = []
        with open(pic_name, 'rb') as f:
            for i in f.read():
                b.append(i)
        return b

    # 判断是否在首页
    def judge_is_home(self):
        if self.d(text='首页').exists():
            self.d(text='首页').click()
            return
        else:
            print('不在首页 应用重启')
            XhsSearch.app_start(self)

    # 返回首页
    def come_back_home(self):
        for i in range(1, 5):
            if self.d(text='首页').exists():
                return
            else:
                self.d.press("back")
                time.sleep(1)

    # 点击 我  版面
    def random_click(self):
        if self.d(text='我').exists():
            self.d(text='我').click()

    # 重新激活qpy3后台程序
    def active_qpy3(self):
        pass

    def execute_do(self):
        while True:
            try:
                # 判断是否在首页
                XhsSearch.come_back_home(self)
                re = requests.post(self.get_xhs_url, headers=self.headers, data=json.dumps(self.body))
                if re.status_code == 200:
                    text = re.text
                    if '任务为空' in text:
                        # 随机关键词搜索
                        XhsSearch.update_phone(self, self.typecode, '无任务', self.phonecode)
                        time.sleep(5 * 60)
                        self.d.healthcheck()
                        # XhsSearch.random_click(self)
                        XhsSearch.app_start(self)
                        continue
                    text = json.loads(text)
                    # 请求成功
                    b = XhsSearch.key_world_search(self, text['KeyWord'], text['Title'])
                    if b:
                        if not self.location:
                            XhsSearch.update_phone(self, self.typecode, '获取Location为空', self.phonecode)
                            continue
                        body = {
                            'PicStr': json.dumps(b)
                        }
                        req = requests.post(pic_change_url, headers=self.headers, data=json.dumps(body))
                        if req.status_code == 200:
                            # 生成url
                            url = json.loads(req.text)
                            handlepic_body = {
                                'TaskId': text['TaskId'],
                                'LogId': text['Id'],
                                'TypeCode': text['TypeCode'],
                                'Left': self.location['bounds']['left'],
                                'LeftTop': self.location['bounds']['top'],
                                'Right': self.location['bounds']['right'],
                                'RightBottom': self.location['bounds']['bottom'],
                                'PicUrl': url,
                                'Message': str(self.number),  # 排名
                                'WorkTime': '',
                                'FinishTime': '',
                                'CreateTime': '',
                                'ReMark': '',
                                'Status': '0'
                            }
                            req = requests.post(pic_handle_insert_url, headers=self.headers,
                                                data=json.dumps(handlepic_body))
                    else:
                        body = {
                            'Id': '%s' % text['Id'],
                            'TaskId': '%s' % text['TaskId'],
                            'TypeCode': text['TypeCode'],
                            'PicCheck': '',
                            'Message': '截图失败',
                            'Number': 0
                        }
                        XhsSearch.update_phone(self, self.typecode, '截图失败 KeyWorld:%s' % text['KeyWord'],
                                               self.phonecode)
                        requests.post(self.submit_url, headers=self.headers, data=json.dumps(body))
                else:
                    print('状态码不对：%s' % re.status_code)
                XhsSearch.come_back_home(self)
                XhsSearch.update_phone(self, self.typecode, '执行结束更新', self.phonecode)
            except Exception as e:
                XhsSearch.update_phone(self, self.typecode, e, self.phonecode)
                print(e)


if __name__ == '__main__':
    xhs = XhsSearch()
    # xhs.key_world_search('婚纱', '为什么结婚一定要穿高贵的婚纱', '成都婚纱照风格')
    xhs.execute_do()

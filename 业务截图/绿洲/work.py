# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import uiautomator2 as u2
import os
import time
import uuid
import requests
import json
import datetime

# 绿洲seo
oasis_seo_url = 'http://222.185.251.62:22027/api/GetLvZhouData'
oasis_seo_submit_url = 'http://222.185.251.62:22027/api/UpdateLvZhouPicCheck'

# 绿洲业务管理
# oasis_type_url = 'http://v3.jqsocial.com:22025/api/common/oasis/getshot?code=jeqeehot'
# oasis_type_submit_url = 'http://v3.jqsocial.com:22025/api/common/oasis/postshot'

oasis_type_url = 'http://222.185.251.62:22027/api/business/getlvzhoushot'
oasis_type_submit_url = 'http://222.185.251.62:22027/api/business/submitlvzhoushot'

pic_handle_insert_url = 'http://222.185.251.62:22027/api/phone/pichandle'
pic_change_url = 'http://222.185.251.62:22027/api/phone/getpicurl'
code = 'jeqeehot'


class OasisSeo(object):
    def __init__(self):
        # self.d = u2.connect_usb('8c5a04d2')
        self.d = u2.connect_wifi('http://0.0.0.0')
        self.d.screen_on()
        self.d.set_new_command_timeout(timeout=300000)
        self.d.watcher("ALERT").when(text="取消").click()
        self.d.watcher("ALERT").when(text="下次再说").click()
        self.d.watcher("ALERT").when(text="以后再说").click()
        # self.d.healthcheck()
        self.body = {'PhoneCode': '小米手机09'}
        self.headers = {'Content-Type': 'application/json'}
        self.typecode = '绿洲SEO'
        self.typecode2 = '绿洲业务管理'
        self.phonecode = '小米手机09'
        self.update_phone_url = 'http://222.185.251.62:22027/api/phone/updatephoneinfo'
        self.location = {}
        OasisSeo.open_app(self)

    def update_phone(self, typecode, logtype, phone_code):
        body = {
            "PhoneCode": phone_code,
            "TypeCode": typecode,
            "Message": "检测手机状态",
            "LogType": logtype
        }
        requests.post(self.update_phone_url, headers=self.headers, data=json.dumps(body))

    def open_app(self):
        if not self.d.app_wait('com.sina.oasis', front=True, timeout=10):
            self.d.app_start('com.sina.oasis', use_monkey=True)
            time.sleep(10)
        if self.d(text='跳过').exists():
            self.d(text='跳过').click()
        if self.d(text='下次再说').exists():
            self.d(text='下次再说').click()
        if self.d(resourceId='com.sina.oasis:id/home').exists():
            print('存在home按钮 app打开成功')
        else:
            if not OasisSeo.come_back_home(self):
                print('home 按钮 不存在 尝试重新登录')
                OasisSeo.open_app(self)

    # 检测相关文字匹配
    def check_text(self):
        for i in range(1, 3):
            if self.d(text='相关动态').exists():
                return True
            self.d.press('back')
            time.sleep(1)
        return False

    # 图片转字节
    def pic_to_byte(self, pic_name):
        b = []
        with open(pic_name, 'rb') as f:
            for i in f.read():
                b.append(i)
        return b

    # 返回Home页
    def come_back_home(self):
        for i in range(1, 5):
            if self.d(resourceId='com.sina.oasis:id/home').exists():
                return True
            else:
                self.d.press("back")
                time.sleep(1)
        return False

    # 关键词搜索
    def search_key(self, search_content):
        try:
            if not self.d(resourceId='com.sina.oasis:id/discovery').exists():
                OasisSeo.open_app(self)
                return ''
            self.d(resourceId='com.sina.oasis:id/discovery').click()
            time.sleep(3)
            self.d(className="android.widget.RelativeLayout").sibling(text="搜索用户、动态和主题").click()
            time.sleep(2)
            # 搜索
            self.d(className='android.widget.EditText').click()
            time.sleep(3)
            self.d(className='android.widget.EditText').send_keys(search_content)
            # self.d.set_fastinput_ime(False)
            time.sleep(2)
            self.d.press('back')
            if not OasisSeo.check_text(self):
                OasisSeo.open_app(self)
                return ''
            if self.d(text='相关动态').exists():
                info = self.d(text='相关动态').info
                top = info['bounds']['top']
                self.d(text='相关动态').gesture(
                    (0, top),
                    (0, top),
                    (0, 379),
                    (0, 379))
                time.sleep(3)
                # 截图
                name = str(uuid.uuid1()) + '.png'
                self.d.screenshot(name)
                b = OasisSeo.pic_to_byte(self, name)
                os.remove(name)
                # 返回home页
                OasisSeo.come_back_home(self)
                return b
        except Exception as e:
            OasisSeo.update_phone(self, self.typecode, e, self.phonecode)
            OasisSeo.open_app(self)
        return ''

    # 笔记查询SEO
    def search_note(self, search_key, content, nickname):
        try:
            if not self.d(resourceId='com.sina.oasis:id/discovery').exists():
                return ''
            self.d(resourceId='com.sina.oasis:id/discovery').click()
            time.sleep(3)
            self.d(className="android.widget.RelativeLayout").sibling(text="搜索用户、动态和主题").click()
            time.sleep(2)
            self.d(className='android.widget.EditText').click()
            time.sleep(3)
            self.d(className='android.widget.EditText').send_keys(search_key)
            time.sleep(5)
            self.d.press('back')
            if not OasisSeo.check_text(self):
                OasisSeo.open_app(self)
                return ''
            if not self.d(text='相关动态').exists():
                self.d.swipe_ext("up", scale=0.3)
            info = self.d(text='相关动态').info
            top = info['bounds']['top']
            self.d(text='相关动态').gesture(
                (0, top),
                (0, top),
                (0, 379),
                (0, 379))
            find = False
            for i in range(0, 10):
                if find:
                    break
                for ele in self.d(className='android.widget.TextView'):
                    if content:
                        if self.d(text=content).exists():
                            info = self.d(text=content).info
                            find = True
                            self.location = {}
                            self.d(text=content).gesture(
                                (0, info['bounds']['top']),
                                (0, info['bounds']['top']),
                                (0, 1200),
                                (0, 1200))
                            # 获取内容位置信息
                            if self.d(text=content).exists():
                                self.location = self.d(text=content).info
                            break
                    if nickname:
                        if self.d(text=nickname).exists():
                            info = self.d(text=nickname).info
                            self.location = {}
                            find = True
                            self.d(text=nickname).gesture(
                                (0, info['bounds']['top']),
                                (0, info['bounds']['top']),
                                (0, 1200),
                                (0, 1200))
                            if self.d(text=nickname).exists():
                                self.location = self.d(text=nickname).info
                            break
                if not find:
                    self.d.swipe_ext("up", scale=0.3)
                time.sleep(4)
            # 截图
            if find:
                time.sleep(2)
                name = str(uuid.uuid1()) + '.png'
                self.d.screenshot(name)
                b = OasisSeo.pic_to_byte(self, name)
                os.remove(name)
                # 返回home页
                OasisSeo.come_back_home(self)
                return b
            else:
                return ''
        except Exception as e:
            OasisSeo.update_phone(self, self.typecode, '截图异常', self.phonecode)

    def judge_home(self):
        for i in range(1, 5):
            if self.d(text='首页').exists():
                return
            else:
                self.d.press("back")
                time.sleep(1)

    # 绿洲业务管理截图
    def typecode_execute(self):
        try:
            req = requests.post(oasis_type_url, headers=self.headers, data=json.dumps(code))
            if req.status_code == 200:
                res = json.loads(req.text)
                if '任务为空' in req.text:
                    return '任务为空'
                res = json.loads(res)
                for key in res:
                    bt = OasisSeo.search_key(self, key['key'])
                    if not bt:
                        OasisSeo.update_phone(self, self.typecode2, '截图失败', self.phonecode)
                        continue
                    if bt:
                        bt = json.dumps(bt)
                        submit_body = {
                            'Id': key['id'],
                            'Code': 'jeqeehot',
                            'Pic': bt
                        }
                        requests.post(oasis_type_submit_url, headers=self.headers,
                                      data=json.dumps(submit_body))
                        OasisSeo.update_phone(self, self.typecode2, '提交截图成功', self.phonecode)
            else:
                return ''
        except Exception as e:
            OasisSeo.update_phone(self, self.typecode2, e, self.phonecode)
        return ''

    # 绿洲SEO执行
    def seo_execute(self):
        while True:
            try:
                self.d.screen_on()
                print('运行中')
                # 业务管理
                res = OasisSeo.typecode_execute(self)
                request = requests.post(oasis_seo_url, headers=self.headers, data=json.dumps(self.body))
                if request.status_code != 200:
                    print('状态码不对:%s' % request.status_code)
                    continue
                text = request.text
                if '任务为空' in text:
                    print('暂无任务 %s' % (datetime.datetime.now()))
                    OasisSeo.update_phone(self, self.typecode, '无任务', self.phonecode)
                    time.sleep(2 * 60)
                    self.d.healthcheck()
                    OasisSeo.open_app(self)
                    continue
                # if '任务为空' in text:
                #     continue
                text = json.loads(text)
                b = OasisSeo.search_note(self, text['KeyWord'], text['Title'], text['NickName'])
                if b:
                    if not self.location:
                        OasisSeo.update_phone(self, self.typecode, '获取location失败', self.phonecode)
                        continue
                    body = {
                        'PicStr': json.dumps(b)
                    }
                    req = requests.post(pic_handle_insert_url, headers=self.headers, data=json.dumps(body))
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
                            'Message': '',
                            'WorkTime': '',
                            'FinishTime': '',
                            'CreateTime': '',
                            'ReMark': '',
                            'Status': '0'
                        }
                        req = requests.post(pic_handle_insert_url, headers=self.headers,
                                            data=json.dumps(handlepic_body))
                    else:
                        OasisSeo.update_phone(self, self.typecode, '图片转url失败', self.phonecode)
                    # body = {
                    #     'Id': text['Id'],
                    #     'TaskId': text['TaskId'],
                    #     'TypeCode': text['TypeCode'],
                    #     'PicCheck': json.dumps(b),
                    #     'Message': '成功'
                    # }
                    # requests.post(oasis_seo_submit_url, headers=self.headers, data=json.dumps(body))
                    # OasisSeo.update_phone(self, self.typecode, '截图成功', self.phonecode)
                else:
                    body = {
                        'Id': text['Id'],
                        'TaskId': text['TaskId'],
                        'TypeCode': text['TypeCode'],
                        'PicCheck': '',
                        'Message': '截图失败'
                    }
                    requests.post(oasis_seo_submit_url, headers=self.headers, data=json.dumps(body))
                    OasisSeo.update_phone(self, self.typecode, '截图失败', self.phonecode)
            except Exception as e:
                OasisSeo.update_phone(self, self.typecode, '异常:' + str(e), self.phonecode)


if __name__ == '__main__':
    oasis = OasisSeo()
    # oasis.search_note('婚纱', '布罗姆婚纱摄影 波西米亚风格', '摄影师苏白')
    oasis.seo_execute()
    # oasis.search_key('婚纱')
    # oasis.search_note('珠宝定制', '珠宝定制丨最值得入手的大牌珠宝 当下最值得入手的大牌珠宝都在这里啦~', '33号柚子老师')

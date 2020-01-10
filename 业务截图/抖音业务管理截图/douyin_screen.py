# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import uiautomator2 as u2
import time
import uuid
import os
import requests
import json

# d = u2.connect('0.0.0.0')
d = u2.connect('8ed6eadf')  # 连接手机
d.watcher("ALERT").when(text="以后再说").click()

code = 'jeqeehot'


class DouYinSearch(object):
    def __init__(self):
        self.douyin_url = 'http://222.185.251.62:22027/api/business/getdouyinshot'
        self.douyin_submit_url = 'http://222.185.251.62:22027/api/business/submitdouyinshot'
        self.body = {'PhoneCode': '小米手机05'}
        self.headers = {'Content-Type': 'application/json'}
        self.phonecode = '小米手机05'
        self.typecode = '抖音业务管理'
        self.message = ''
        self.update_phone_url = 'http://222.185.251.62:22027/api/phone/updatephoneinfo'
        DouYinSearch.open_dou_yin(self)

    def update_phone(self, typecode, logtype, phone_code):
        body = {
            "PhoneCode": phone_code,
            "TypeCode": typecode,
            "Message": self.message,
            "LogType": logtype
        }
        requests.post(self.update_phone_url, headers=self.headers, data=json.dumps(body))

    # 需要固定在搜索框页面
    def open_dou_yin(self):
        d.screen_on()
        if not d.app_wait('com.ss.android.ugc.aweme'):  # App 处于非运行状态
            d.app_start('com.ss.android.ugc.aweme', use_monkey=True)
            time.sleep(10)
            d.click(0.501, 0.482)
        else:  # App 处于运行状态
            if not DouYinSearch.home_page(self):
                d.session('com.ss.android.ugc.aweme')
                time.sleep(10)
            if d(text='我知道了').exists():
                d(text='我知道了').click()
            d.click(0.501, 0.482)
        time.sleep(3)
        if d(text='我知道了').exists():
            d(text='我知道了').click()
        if d(text='取消').exists():
            d(text='取消').click()

    def home_page(self):
        for i in range(1, 5):
            if d(text='首页').exists():
                return True
            d.press('back')
            time.sleep(2)
        return False

    def pic_to_byte(self, pic_name):
        b = []
        with open(pic_name, 'rb') as f:
            for i in f.read():
                b.append(i)
        return b

    # 抖音搜索关键词
    def douyin_search_keyworld(self, search_content):
        try:
            if not d(className='android.widget.EditText').exists():
                if not d(resourceId='com.ss.android.ugc.aweme:id/ao0').exists():
                    DouYinSearch.open_dou_yin(self)
                    return ''
                else:
                    d(resourceId='com.ss.android.ugc.aweme:id/ao0').click()
            time.sleep(3)
            if d(text='温馨提示').exists():
                if d(text='取消').exists():
                    d(text='取消').click()
            d(className='android.widget.EditText').click()
            time.sleep(10)
            d(className='android.widget.EditText').send_keys(search_content)
            # 输入法搜索按钮位置
            d.click(0.927, 0.952)
            time.sleep(10)
            # 模拟滑动
            for i in range(0, 10):
                d.swipe_ext('up', scale=0.1)
                time.sleep(1)
            for i in range(0, 10):
                d.swipe_ext('down', scale=0.1)
                time.sleep(1)
            if not d(text='搜索结果为空').exists():
                time.sleep(2)
                name = str(uuid.uuid1()) + '.png'
                d.screenshot(name)
                b = DouYinSearch.pic_to_byte(self, name)
                os.remove(name)
                d(className='android.widget.EditText').clear_text()
                return b
            self.message = '搜索结果为空'
            return ''
        except Exception as e:
            print(e)

    # 执行
    def execute(self):
        try:
            while True:
                try:
                    request = requests.post(self.douyin_url, headers=self.headers, data=json.dumps(code))
                    if request.status_code == 200:
                        text = json.loads(request.text)
                        text = json.loads(text)
                        if '任务为空' in request.text:
                            DouYinSearch.update_phone(self, self.typecode, '无任务', self.phonecode)
                            time.sleep(10 * 60)
                            # 检查守护线程 是否运行
                            d.healthcheck()
                            DouYinSearch.open_dou_yin(self)
                            continue
                        print(text)
                        for key in text:
                            self.message = '检测'
                            b = DouYinSearch.douyin_search_keyworld(self, key['key'])
                            if b:
                                json_str = json.dumps(b)
                                submit_body = {
                                    'id': key['id'],
                                    'code': 'jeqeehot',
                                    'pic': json_str
                                }
                                submit = requests.post(self.douyin_submit_url, headers=self.headers,
                                                       data=json.dumps(submit_body))
                                print(submit.text)
                                DouYinSearch.update_phone(self, self.typecode, '截图成功', self.phonecode)
                            else:
                                DouYinSearch.update_phone(self, self.typecode, '截图失败', self.phonecode)
                    else:
                        DouYinSearch.update_phone(self, self.typecode, '状态码:%s' % request.status_code, self.phonecode)
                except Exception as e:
                    print(e)
                    DouYinSearch.update_phone(self, self.typecode, '异常', self.phonecode)
        except Exception as e:
            DouYinSearch.update_phone(self, self.typecode, '异常', self.phonecode)
            print(e)


if __name__ == '__main__':
    douyin = DouYinSearch()
    douyin.execute()
    pass

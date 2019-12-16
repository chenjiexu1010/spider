# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import uiautomator2 as u2
import time
import requests
import json
import uuid
import os

d = u2.connect('0.0.0.0')
# d = u2.connect_usb('f7d64448')
d.set_new_command_timeout(300000)
zhihu_type_url = 'http://v3.jqsocial.com:22025/api/common/zhihu/getshot?code=jeqeehot'
zhihu_type_submit_url = 'http://v3.jqsocial.com:22025/api/common/zhihu/postshot'
update_phone_url = 'http://222.185.251.62:22027/api/phone/updatephoneinfo'
headers = {'Content-Type': 'application/json'}
typecode = '知乎业务管理'
phonecode = '小米手机07'


class ZhiHuScreen(object):
    def __init__(self):
        ZhiHuScreen.open_app(self)

    def open_app(self):
        d.app_start('com.zhihu.android')
        time.sleep(5)
        if d(text='下次再说').exists():
            d(text='下次再说').click()
        if d(resourceId='com.zhihu.android:id/iv_equity_close').exists():
            d(resourceId='com.zhihu.android:id/iv_equity_close').click()
        ZhiHuScreen.judge_search_page(self)
        if d(resourceId='com.smile.gifmaker:id/left_btn').exists():
            d(resourceId='com.smile.gifmaker:id/left_btn').click()

    # 判断是否在搜索页面
    def judge_search_page(self):
        for i in range(1, 5):
            if not d(text='首页').exists():
                d.press('back')
                time.sleep(2)
            else:
                break

    def update_phone(self, message, logtype):
        body = {
            "PhoneCode": phonecode,
            "TypeCode": typecode,
            "Message": message,
            "LogType": logtype
        }
        requests.post(update_phone_url, headers=headers, data=json.dumps(body))

    def pic_to_byte(self, pic_name):
        b = []
        with open(pic_name, 'rb') as f:
            for i in f.read():
                b.append(i)
        return b

    def restart_app(self):
        d.session('com.zhihu.android')
        time.sleep(5)
        ZhiHuScreen.open_app(self)

    def move(self):
        while True:
            info = d(description='话题').info
            top = info['bounds']['top']
            d(className='android.view.View').gesture(
                (0, top),
                (0, top),
                (0, 216),
                (0, 216))
            time.sleep(2)
            if not d(description='话题').exists():
                break
            info = d(description='话题').info
            top = info['bounds']['top']
            if top <= 300:
                break

    def search(self, search_content):
        b = ''
        try:
            d(resourceId='com.zhihu.android:id/input').click()
            time.sleep(2)
            if d(text='下次再说').exists():
                d(text='下次再说').click()
            d(className='android.widget.EditText').send_keys(search_content)
            time.sleep(1)
            d.click(0.921, 0.95)
            time.sleep(20)
            name = str(uuid.uuid1()) + '.png'
            d.screenshot(name)
            b = ZhiHuScreen.pic_to_byte(self, name)
            os.remove(name)
            return b
        except Exception as e:
            ZhiHuScreen.restart_app(self)
        return b

    def execute(self):
        while True:
            try:
                d.app_start('com.zhihu.android')
                request = requests.post(zhihu_type_url)
                if request.status_code == 200:
                    search_dic = json.loads(request.text)
                    if not search_dic['Data']:
                        ZhiHuScreen.update_phone(self, '无任务', '检测')
                        time.sleep(5 * 60)
                        # 检查守护线程 是否运行
                        d.healthcheck()
                        d.app_start('com.zhihu.android')
                        continue
                    for key in search_dic['Data']:
                        bt = ZhiHuScreen.search(self, key['key'])
                        if bt:
                            json_str = json.dumps(bt)
                            submit = requests.post(zhihu_type_submit_url,
                                                   data={'id': key['id'], 'code': 'jeqeehot', 'pic': json_str})
                            ZhiHuScreen.update_phone(self, submit.text, '检测')
                        else:
                            ZhiHuScreen.update_phone(self, '截图失败', '检测')
            except Exception as e:
                print(e)
            pass


if __name__ == '__main__':
    ks = ZhiHuScreen()
    ks.execute()
    pass

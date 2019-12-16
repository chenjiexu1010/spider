# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import uiautomator2 as u2
import time
import requests
import json
import uuid
import os

# d = u2.connect('0.0.0.0')
# d.healthcheck()
d = u2.connect_usb('35954d57')
kuaishou_type_url = 'http://v3.jqsocial.com:22025/api/common/ks/getshot?code=jeqeehot'
kuaishou_type_submit_url = 'http://v3.jqsocial.com:22025/api/common/ks/postshot'
update_phone_url = 'http://222.185.251.62:22027/api/phone/updatephoneinfo'
headers = {'Content-Type': 'application/json'}
typecode = '快手业务管理'
phonecode = '小米手机06'


class KuaiShouScreen(object):
    def __init__(self):
        KuaiShouScreen.open_app(self)

    def open_app(self):
        d.app_start('com.smile.gifmaker')
        time.sleep(10)
        if d(text='妥妥好评').exists():
            d.press('back')
        if d(text='同意').exists():
            d(text='同意').click()
        KuaiShouScreen.judge_search_page(self)
        if d(resourceId='com.smile.gifmaker:id/left_btn').exists():
            d(resourceId='com.smile.gifmaker:id/left_btn').click()
        if d(text='查找').exists():
            d(text='查找').click()

    # 判断是否在搜索页面
    def judge_search_page(self):
        for i in range(1, 5):
            if not d(description='菜单').exists():
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

    def search(self, search_content):
        b = ''
        try:
            d(resourceId='com.smile.gifmaker:id/search_layout').click()
            d(className='android.widget.EditText').send_keys(search_content)
            if d(resourceId='com.smile.gifmaker:id/right_btn_layout').exists():
                d(resourceId='com.smile.gifmaker:id/right_btn_layout').click()
            time.sleep(5)
            if d(text='推荐').exists():
                info = d(text='推荐')
                top = info.info['bounds']['top']
                d(text='推荐').gesture(
                    (0, top),
                    (0, top),
                    (0, 192),
                    (0, 192))
                time.sleep(3)
                name = str(uuid.uuid1()) + '.png'
                d.screenshot(name)
                b = KuaiShouScreen.pic_to_byte(self, name)
                os.remove(name)
            if d(text='综合').exists():
                name = str(uuid.uuid1()) + '.png'
                d.screenshot(name)
                b = KuaiShouScreen.pic_to_byte(self, name)
                os.remove(name)
            d.press('back')
        except Exception as e:
            print(e)
        return b

    def execute(self):
        while True:
            try:
                request = requests.post(kuaishou_type_url)
                if request.status_code == 200:
                    search_dic = json.loads(request.text)
                    if not search_dic['Data']:
                        KuaiShouScreen.update_phone(self, '无任务', '检测')
                        time.sleep(10 * 60)
                        # 检查守护线程 是否运行
                        d.healthcheck()
                        d.app_start('com.smile.gifmaker')
                        continue
                    for key in search_dic['Data']:
                        bt = KuaiShouScreen.search(self, key['key'])
                        if bt:
                            json_str = json.dumps(bt)
                            submit = requests.post(kuaishou_type_submit_url,
                                                   data={'id': key['id'], 'code': 'jeqeehot', 'pic': json_str})
                            print(submit)
                            KuaiShouScreen.update_phone(self, '截图成功', '检测')
                        else:
                            KuaiShouScreen.update_phone(self, '截图失败', '检测')
            except Exception as e:
                print(e)
            pass


if __name__ == '__main__':
    ks = KuaiShouScreen()
    ks.execute()
    pass

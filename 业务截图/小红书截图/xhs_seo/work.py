# -*- coding:utf-8 -*-
# !/usr/bin/Python3

import uiautomator2 as u2
import time
import os
import uuid
import requests
import json
import datetime


class XhsScreenHot(object):
    def __init__(self):
        # os.system("su root am start -n com.github.uiautomator/.MainActivity")
        self.d = u2.connect('http://0.0.0.0')
        # self.d = u2.connect_usb('a4264501')
        self.d.set_new_command_timeout(300000)
        # self.d.healthcheck()
        self.typecode = '小红书业务管理'
        # self.d = u2.connect_usb('a4264501')
        self.d.watcher("ALERT").when(text="取消").click()
        self.d.watcher("ALERT").when(text="下次再说").click()
        self.screen_hot1_url = 'http://v3.jqsocial.com:22025/api/common/getshot?code=jeqeehot'
        self.screen_hot1_submit_url = 'http://v3.jqsocial.com:22025/api/common/postshot'
        # 更新手机信息url
        self.headers = {'Content-Type': 'application/json'}
        self.phone_code = '小米手机01'
        self.update_phone_url = 'http://222.185.251.62:22027/api/phone/updatephoneinfo'
        print("手机连接成功")
        XhsScreenHot.app_start(self)

    # 启动app
    def app_start(self):
        print('app重启')
        self.d.screen_on()
        self.d.app_start('com.xingin.xhs')
        time.sleep(10)
        exist = self.d(text='取消').exists()
        if exist:
            self.d(text='取消').click()
            time.sleep(2)

    # 判读是否在首页
    def judge_home(self):
        for i in range(1, 5):
            if self.d(text='首页').exists:
                break
            self.d.press('back')
            time.sleep(3)

    # 处理搜狗弹窗
    def sougou_popup(self):
        is_exists = self.d(text='下次再说').exists
        if is_exists:
            self.d(text='下次再说').click()
            time.sleep(1)

    # 搜索关键词截图
    def xhs_search_screen(self, key_world):
        try:
            XhsScreenHot.judge_home(self)
            # 搜索框是否存在
            search = self.d(resourceId='com.xingin.xhs:id/b4b').exists
            if not search:
                XhsScreenHot.app_start(self)
                return
            self.d(resourceId='com.xingin.xhs:id/b4b').click(timeout=5)
            time.sleep(3)
            search_two = self.d(className='android.widget.EditText').exists()
            if not search_two:
                XhsScreenHot.app_start(self)
                return
            self.d(className='android.widget.EditText').send_keys(key_world)
            self.d(text='搜索').click()
            time.sleep(5)
            n = str(uuid.uuid1()) + '.png'
            self.d.screenshot(n)
            b = XhsScreenHot.pic_to_byte(self, n)
            os.remove(n)
            self.d.press("back")
            time.sleep(1)
            self.d.press("back")
            time.sleep(1)
            self.d.press("back")
            time.sleep(1)
            return b
        except Exception as e:
            print(e)
            XhsScreenHot.app_start(self)

    # 搜索关键词并进入第一篇笔记截图
    def xhs_search_news_screen(self, key_world):
        try:
            # 搜索框是否存在
            search = self.d(resourceId='com.xingin.xhs:id/b2y').exists
            if not search:
                XhsScreenHot.app_start(self)
                return
            self.d(resourceId='com.xingin.xhs:id/b2y').click(timeout=3)
            time.sleep(5)
            search_two = self.d(resourceId='com.xingin.xhs:id/b4g').exists()
            if not search_two:
                XhsScreenHot.app_start(self)
                return
            print('准备开始搜索:' + key_world)
            self.d(resourceId='com.xingin.xhs:id/b4g').send_keys(key_world)
            print('输入关键词成功')
            self.d(text='搜索').click()
            time.sleep(5)
            is_isexst = self.d(resourceId='com.xingin.xhs:id/b21').exists()
            if not is_isexst:
                XhsScreenHot.app_start(self)
                return
            time.sleep(3)
            new_exists = self.d(text='最新').exists()
            if not new_exists:
                XhsScreenHot.app_start(self)
                return
            self.d(text='最新').click()
            time.sleep(5)
            self.d.click(0.262, 0.479)
            time.sleep(5)
            n = str(uuid.uuid1()) + '.png'
            self.d.screenshot(n)
            b = XhsScreenHot.pic_to_byte(self, n)
            os.remove(n)
            self.d.press("back")
            time.sleep(1)
            self.d.press("back")
            time.sleep(1)
            self.d.press("back")
            time.sleep(1)
            self.d.press("back")
            time.sleep(1)
            return b
        except Exception as e:
            print(e)

    # 图片转字节
    def pic_to_byte(self, name):
        b = []
        with open(name, 'rb') as f:
            for i in f.read():
                b.append(i)
        return b

    def update_phone(self, typecode, logtype, phone_code):
        body = {
            "PhoneCode": phone_code,
            "TypeCode": typecode,
            "Message": "检测手机状态",
            "LogType": logtype
        }
        requests.post(self.update_phone_url, headers=self.headers, data=json.dumps(body))

    # 判断执行哪个方法
    def judge_execute(self):
        while True:
            try:
                bt = ''
                # 请求
                request = requests.post(self.screen_hot1_url)
                # 请求成功  200 SEO 截图首页   201 代运营搜索关键词截取第一篇笔记
                if request.status_code == 200:
                    search_dic = json.loads(request.text)
                    i = 0
                    if not search_dic['Data']:
                        print('暂无任务 %s' % (datetime.datetime.now()))
                        XhsScreenHot.update_phone(self, self.typecode, '无任务', self.phone_code)
                        time.sleep(1 * 60)
                        self.d.healthcheck()
                        # 检查守护线程 是否运行
                        XhsScreenHot.app_start(self)
                        continue
                    print('获取到任务长度:%s' % (len(search_dic['Data'])))
                    for key in search_dic['Data']:
                        try:
                            i += 1
                            print('当前已执行%s/%s' % (i, len(search_dic['Data'])))
                            if key['typecode'] == 'JQHOT_0200':
                                bt = XhsScreenHot.xhs_search_screen(self, key['key'])
                                if not bt:
                                    continue
                            if key['typecode'] == 'JQHOT_0201':
                                bt = XhsScreenHot.xhs_search_news_screen(self, key['key'])
                                if not bt:
                                    continue
                            # 提交
                            json_str = json.dumps(bt)
                            submit = requests.post(self.screen_hot1_submit_url,
                                                   data={'id': key['id'], 'code': 'jeqeehot', 'pic': json_str})
                            XhsScreenHot.update_phone(self, self.typecode, '提交任务', self.phone_code)
                            print(submit.text + '%s：提交一条任务' % key['typecode'])
                        except Exception as e:
                            print(e)
                            XhsScreenHot.app_start(self)
                else:
                    print(request.status_code)
            except Exception as e:
                print(e)
                XhsScreenHot.app_start(self)
            time.sleep(10)
            XhsScreenHot.app_start(self)
            # 更新手机使用时间


if __name__ == '__main__':
    try:
        xhs = XhsScreenHot()
        # xhs.xhs_search_screen('婚纱')
        xhs.judge_execute()
    except Exception as e:
        print(e)
    pass

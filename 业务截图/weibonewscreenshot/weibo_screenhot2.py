# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import uiautomator2 as ui2
import os
import time
import uuid
import requests
import json

# 微博包名
PACKAGE_NAME = 'com.sina.weibo'
# 获取任务
get_task_url = 'http://222.185.251.62:22027/api/GetWeiBoShotData'
# 提交任务
submit_task_url = 'http://222.185.251.62:22027/api/PostWeiBoShotData'
# 请求头参数
header = {'Content-Type': 'application/json'}

'''
   添加微博昵称判断
'''


class WeiBoScreenShot(object):
    def __init__(self):
        self.count = 5
        self.time_count = 10
        # self.driver = ui2.connect_usb('91a4356b')
        # 本机
        self.driver = ui2.connect('http://0.0.0.0')
        # 注册监听事件
        self.driver.watcher("ALERT").when(text='取消').click()
        self.driver.watcher("ALERT").when(text='下次再说').click()
        self.driver.watcher("ALERT").when(text='以后再说').click()
        # 启动App
        self.open_app_ready()
        time.sleep(5)

    # 打开app
    def open_app_ready(self):
        self.driver.screenshot()
        self.driver.app_start(PACKAGE_NAME)
        time.sleep(10)
        # 广告处理
        exist = self.driver(resourceId='com.sina.weibo:id/rl_content').exists()
        if exist:
            self.driver(resourceId='com.sina.weibo:id/rl_content').click()

    # 热门截图
    def hot_screen_hot(self, search_key, search_content, search_nickname):
        self.driver.screen_on()
        res = b''
        hot_find = False
        i = 0
        # 搜索关键词
        WeiBoScreenShot.search(self, search_content=search_key)
        # 判断是否在综合页面
        if not self.driver(text='综合').exists():
            return res
        while True:
            try:
                if i >= self.count or hot_find:
                    break
                while True:
                    if i >= self.count:
                        self.driver.press('back')
                        break
                    exist = self.driver(text='热门').exists
                    # 找到热门版面
                    if exist:
                        i += 1
                        hot_info = self.driver(text='热门').info
                        # 指定热门版面
                        self.driver(text="热门").gesture((hot_info['bounds']['left'], hot_info['bounds']['top']),
                                                       (hot_info['bounds']['left'], hot_info['bounds']['top']),
                                                       (0, 359), (0, 359))
                        # 博文内容是否存在
                        is_exists = self.driver(resourceId='com.sina.weibo:id/contentTextView').exists()
                        if is_exists:
                            # 存在博文内容
                            info = self.driver(resourceId='com.sina.weibo:id/contentTextView').info
                            if not info:
                                continue
                            # 判断是否匹配到微博内容
                            if search_content in info['contentDescription']:
                                # 移动到截图位置
                                info2 = self.driver(resourceId='com.sina.weibo:id/contentTextView').info
                                self.driver(resourceId='com.sina.weibo:id/contentTextView').gesture(
                                    (info2['bounds']['left'], info2['bounds']['top']),
                                    (info2['bounds']['left'], info2['bounds']['top']),
                                    (0, 459),
                                    (0, 459))
                                time.sleep(2)
                                # TODO 先判断微博昵称 模糊点击昵称 d.click(0.085, 0.227)
                                self.driver.click(0.085, 0.227)
                                time.sleep(2)
                                if self.driver(text='主页').exists() and self.driver(text=search_nickname).exists():
                                    self.driver.press('back')
                                    # TODO 不小心点击到超链接 回退处理
                                    if not self.driver(text='综合').exists():
                                        self.driver.press('back')
                                    time.sleep(5)
                                    is_true = WeiBoScreenShot.judge_screen_page(self)
                                    if is_true:
                                        pic_name = str(uuid.uuid1()) + '.png'
                                        self.driver.screenshot(pic_name)
                                        res = WeiBoScreenShot.pic_to_byte(pic_name)
                                        os.remove(pic_name)
                                        self.driver.press('back')
                                        hot_find = True
                                        print('热门截图成功 %s' % search_key)
                                        break
                                else:
                                    self.driver.press('back')
                                    print('微博昵称不匹配, 截图失败')
                            else:
                                self.driver.swipe_ext('up', scale=0.3)
                                time.sleep(2)
                        print('未找到博文对应内容 程序返回')
                    else:
                        if i >= 1:
                            i += 1
                        self.driver.swipe_ext('up', scale=0.2)
                        time.sleep(3)
            except Exception as e:
                print(e)
        return res

    # 实时截图
    def time_screen_hot(self, search_key, search_content, search_nickname):
        res = b''
        blog = ''
        self.driver.screen_on()
        time_find = False
        i = 0
        # 搜索关键词
        WeiBoScreenShot.search(self, search_content=search_key)
        while True:
            if i >= self.time_count or time_find:
                break
            is_exists = self.driver(text='实时微博').exists()
            if not is_exists:
                # 下移搜索
                self.driver.swipe_ext('up', scale=0.3)
                time.sleep(2)
                continue
            else:
                # 搜索实时微博版面
                realtime_info = self.driver(text='实时微博').info
                left = realtime_info['bounds']['left']
                top = realtime_info['bounds']['top']
                # 置顶实时版面
                self.driver(text='实时微博').gesture((left, top),
                                                 (left, top),
                                                 (0, 359), (0, 359))
                time.sleep(2)
                while True:
                    try:
                        if i >= self.time_count:
                            print('搜索达到上限')
                            self.driver.press('back')
                            break
                        blog_exists = self.driver(resourceId='com.sina.weibo:id/contentTextView').exists()
                        if not blog_exists:
                            self.driver.swipe_ext('up', scale=0.2)
                        info = self.driver(resourceId='com.sina.weibo:id/contentTextView').info
                        if blog in info['contentDescription'] and blog.strip() != '':
                            # 下滑
                            self.driver.swipe_ext('up', scale=0.2)
                            time.sleep(1)
                            continue
                        else:
                            blog = info['contentDescription']
                        i += 1
                        # 搜索到对应内容
                        if search_content in info['contentDescription']:
                            top = info['bounds']['top']
                            self.driver(resourceId='com.sina.weibo:id/contentTextView').gesture(
                                (left, top),
                                (left, top),
                                (0, 459),
                                (0, 459))
                            self.driver.click(0.085, 0.227)
                            time.sleep(3)
                            if self.driver(text='主页').exists() and self.driver(text=search_nickname).exists():
                                self.driver.press('back')
                                left = info['bounds']['left']
                                time.sleep(3)
                                # TODO 不小心点击到超链接 回退处理
                                if not self.driver(text='综合').exists():
                                    self.driver.press('back')
                                # TODO 截图
                                is_true = WeiBoScreenShot.judge_screen_page(self)
                                if is_true:
                                    pic_name = str(uuid.uuid1()) + '.png'
                                    self.driver.screenshot(pic_name)
                                    time_find = True
                                    res = WeiBoScreenShot.pic_to_byte(pic_name)
                                    os.remove(pic_name)
                                    self.driver.press('back')
                                    print('实时截图成功 %s' % search_key)
                                    break
                            else:
                                self.driver.press('back')
                                print('实时截图失败 微博昵称不匹配')
                        else:
                            blog = info['contentDescription']
                            self.driver.swipe_ext('up', scale=0.2)
                            time.sleep(1)
                    except Exception as e:
                        print(str(e))
        return res

    # 搜索关键词
    def search(self, search_content):
        try:
            # 判断是否在搜索页面
            WeiBoScreenShot.judge_home(self)
            # 是否存在弹窗
            close = self.driver(resourceId='com.sina.weibo:id/iv_close').exists()
            if close:
                self.driver(resourceId='com.sina.weibo:id/iv_close').click()
            # 点击发现
            self.driver(description='发现').click()
            time.sleep(2)
            self.driver(resourceId='com.sina.weibo:id/tv_search_keyword').click()
            time.sleep(3)
            self.driver(resourceId='com.sina.weibo:id/tv_search_keyword').send_keys(search_content)
            # 点击输入法搜索 (点击指定坐标)
            self.driver.click(0.929, 0.963)
            time.sleep(3)
        except Exception as e:
            self.driver.press('back')

    # 判断截图页面
    def judge_screen_page(self):
        if self.driver(text='主页').exists() or self.driver(text='微博正文').exists():
            return False
        if not self.driver(className="android.view.ViewGroup").sibling(text="讨论").exists():
            return False
        return True

    # 图片转字节
    @staticmethod
    def pic_to_byte(pic_name):
        b = []
        with open(pic_name, 'rb') as f:
            for i in f.read():
                b.append(i)
        return b

    # 判断首页
    def judge_home(self):
        for i in range(1, 5):
            if self.driver(description='发现').exists():
                return
            else:
                self.driver.press('back')

    # 执行主体
    def execute(self):
        try:
            while True:
                try:
                    # 判断是否在发现页
                    WeiBoScreenShot.judge_home(self)
                    body = {
                        'PhoneCode': '小米手机01'
                    }
                    re = requests.post(get_task_url, headers=header, data=json.dumps(body))
                    # 请求成功
                    if re.status_code == 200:
                        text = json.loads(re.text)
                        print(text)
                        if '任务存在' not in text['Message']:
                            time.sleep(2 * 60)
                            self.driver.healthcheck()
                            WeiBoScreenShot.open_app_ready(self)
                            continue
                        body = {
                            'WeiBoTaskId': '%s' % text['WeiBoTaskId'],
                            'WeiBoTargetId': '%s' % text['WeiBoTargetId'],
                            'PicStr': '',
                            'TypeCode': text['TypeCode'],
                            'Message': ''
                        }
                        # 热门
                        if text['TypeCode'] == 'JQHOT_0101':
                            b = WeiBoScreenShot.hot_screen_hot(self, text['Keyword'], text['Content'], text['NickName'])
                            if b:
                                body['PicStr'] = json.dumps(b)
                                body['Message'] = '成功'
                                requests.post(submit_task_url, headers=header, data=json.dumps(body))
                            else:
                                body['Message'] = '截图失败'
                                print('截图失败')
                                requests.post(submit_task_url, headers=header, data=json.dumps(body))
                        # 实时
                        if text['TypeCode'] == 'JQHOT_0100':
                            b = WeiBoScreenShot.time_screen_hot(self, text['Keyword'], text['Content'],
                                                                text['NickName'])
                            if b:
                                body['PicStr'] = json.dumps(b)
                                body['Message'] = '成功'
                                requests.post(submit_task_url, headers=header, data=json.dumps(body))
                                print('实时提交一条任务')
                            else:
                                body['Message'] = '截图失败'
                                print('实时截图失败')
                                requests.post(submit_task_url, headers=header, data=json.dumps(body))
                            pass
                    else:
                        print('状态码: %s' % re.status_code)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    xhs = WeiBoScreenShot()
    # xhs.hot_screen_hot('莆田鞋', '', '')
    # xhs.time_screen_hot('莆田鞋', '', '')
    xhs.execute()

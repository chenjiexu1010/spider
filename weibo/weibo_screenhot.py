# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import uiautomator2 as ui2
import os
import time
import uuid
import requests
import json

PACKAGE_NAME = 'com.sina.weibo'


class WeiBoScreenShot(object):

    def __init__(self, serial):
        self.count = 3
        self.time_count = 10
        self.driver = ui2.connect_usb(serial)
        # if isinstance(self.driver, Device):
        #     assert '类型不对'
        self.driver.watcher("ALERT").when(text='取消').click()
        self.driver.watcher("ALERT").when(text='下次再说').click()
        self.driver.watcher("ALERT").when(text='以后再说').click()
        # self.driver = ui2.connect('http://0.0.0.0')
        self.get_url = 'http://222.185.251.62:22027/api/GetWeiBoShotData'
        self.submit_url = 'http://222.185.251.62:22027/api/PostWeiBoShotData'
        self.headers = {'Content-Type': 'application/json'}
        self.open_app_ready()
        time.sleep(5)

    # 打开app
    def open_app_ready(self):
        self.driver.screen_on()
        self.driver.app_start(PACKAGE_NAME)
        time.sleep(10)
        # 打开app 弹窗
        exist = self.driver(resourceId='com.sina.weibo:id/rl_content').exists()
        if exist:
            self.driver.xpath('//*[@resource-id="com.sina.weibo:id/iv_close"]').click()
        if self.driver(text='以后再说').exists():
            self.driver(text='以后再说').click()

    # 重启app
    def restart_app(self):
        self.driver.session('PACKAGE_NAME')
        time.sleep(8)

    # 热门截图
    def hot_screen_hot(self, search_key, search_content):
        res = b''
        # 判断屏幕状态
        self.driver.screen_on()
        hot_find = False
        i = 0
        # 搜索关键词
        WeiBoScreenShot.search(self, search_content=search_key)
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
                        # 将热门置顶
                        hot_info = self.driver(text='热门').info
                        left = hot_info['bounds']['left']
                        top = hot_info['bounds']['top']
                        self.driver(text="热门").gesture((left, top),
                                                       (left, top),
                                                       (0, 287), (0, 287))
                        is_exists = self.driver(resourceId='com.sina.weibo:id/contentTextView').exists()
                        if is_exists:
                            info = self.driver(resourceId='com.sina.weibo:id/contentTextView').info
                            if not info:
                                continue
                            # 找到对应博文  search_content in info['contentDescription']
                            if search_content in info['contentDescription']:
                                info2 = self.driver(resourceId='com.sina.weibo:id/contentTextView').info
                                left = info2['bounds']['left']
                                top = info2['bounds']['top']
                                self.driver(resourceId='com.sina.weibo:id/contentTextView').gesture(
                                    (left, top),
                                    (left, top),
                                    (0, 459),
                                    (0, 459))
                                time.sleep(5)
                                # TODO 截图
                                is_true = WeiBoScreenShot.judge_screen_page(self)
                                if is_true:
                                    pic_name = str(uuid.uuid1()) + '.jpg'
                                    self.driver.screenshot(pic_name)
                                    # TODO 上传图片到图片服务器
                                    res = WeiBoScreenShot.pic_to_byte(self, pic_name)
                                    # 删除本地文件
                                    os.remove(pic_name)
                                    self.driver.press('back')
                                    hot_find = True
                                    print('热门截图成功 %s' % search_key)
                                    break
                                else:
                                    print('截图不在对应版面')
                            else:
                                # 内容不匹配 下移
                                self.driver.swipe_ext('up', scale=0.5)
                                time.sleep(2)
                    else:
                        if i >= 1:
                            i += 1
                        # 下移
                        self.driver.swipe_ext('up', scale=0.2)
                        time.sleep(3)
                        continue
            except Exception as e:
                print(e)
                break
                # WeiBoScreenShot.restart_app(self)
        return res

    # 实时截图
    def time_screen_hot(self, search_key, search_content):
        res = b''
        blog = ''
        # 判断屏幕状态
        on = self.driver.info.get('screenOn')
        if not on:
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
                                                 (0, 287), (0, 287))
                time.sleep(2)
                while True:
                    try:
                        if i >= self.time_count:
                            print('搜索达到上限')
                            self.driver.press('back')
                            break
                        # 获取节点详细信息
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
                        # 找到不同博文 search_content in info['contentDescription']
                        if search_content in info['contentDescription']:
                            left = info['bounds']['left']
                            top = info['bounds']['top']
                            self.driver(resourceId='com.sina.weibo:id/contentTextView').gesture(
                                (left, top),
                                (left, top),
                                (0, 459),
                                (0, 459))
                            time.sleep(5)
                            # TODO 截图
                            is_true = WeiBoScreenShot.judge_screen_page(self)
                            if is_true:
                                pic_name = str(uuid.uuid1()) + '.jpg'
                                self.driver.screenshot(pic_name)
                                time_find = True
                                # TODO 上传图片到图片服务器
                                res = WeiBoScreenShot.pic_to_byte(self, pic_name)
                                # 删除本地文件
                                os.remove(pic_name)
                                self.driver.press('back')
                                print('实时截图成功 %s' % search_key)
                                break
                            else:
                                pass
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
            time.sleep(2)
            WeiBoScreenShot.update(self)
            WeiBoScreenShot.sougou_popup(self)
            # 是否存在弹窗
            close = self.driver(resourceId='com.sina.weibo:id/iv_close').exists()
            if close:
                self.driver(resourceId='com.sina.weibo:id/iv_close').click()
            # 点击发现
            self.driver.xpath('//*[@content-desc="发现"]').click(timeout=20)
            time.sleep(2)
            self.driver(resourceId='com.sina.weibo:id/tv_search_keyword').click()
            time.sleep(3)
            # 判断搜狗书输入发弹窗
            WeiBoScreenShot.sougou_popup(self)
            self.driver(resourceId='com.sina.weibo:id/tv_search_keyword').send_keys(search_content)
            # 点击输入法搜索
            self.driver.click(0.929, 0.963)
            time.sleep(3)
        except Exception as e:
            self.driver.press('back')
            WeiBoScreenShot.search(self, search_content)

    # 判断截图页面
    def judge_screen_page(self):
        if self.driver(text='主页').exists() or self.driver(text='微博正文').exists():
            return False
        if not self.driver(className="android.view.ViewGroup").sibling(text="讨论").exists():
            return False
        return True

    # 图片转字节
    def pic_to_byte(self, pic_name):
        b = []
        with open(pic_name, 'rb') as f:
            for i in f.read():
                b.append(i)
        return b

    # 处理搜狗弹窗
    def sougou_popup(self):
        is_exists = self.driver(text='下次再说').exists
        if is_exists:
            self.driver(text='下次再说').click()
            time.sleep(1)

    def update(self):
        exists = self.driver(text='以后再说').exists()
        if exists:
            self.driver(text='以后再说').click()

    # 判断首页
    def judge_home(self):
        for i in range(1, 5):
            if self.driver(description='发现').exists():
                return
            else:
                self.driver.press('back')
        pass

    # 执行
    def execute(self):
        try:
            while True:
                try:
                    WeiBoScreenShot.judge_home(self)
                    body = {
                        'PhoneCode': '小米手机01'
                    }
                    re = requests.post(self.get_url, headers=self.headers, data=json.dumps(body))
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
                            b = WeiBoScreenShot.hot_screen_hot(self, text['Keyword'], text['Content'])
                            if b:
                                body['PicStr'] = json.dumps(b)
                                body['Message'] = '成功'
                                requests.post(self.submit_url, headers=self.headers, data=json.dumps(body))
                            else:
                                body['Message'] = '截图失败'
                                print('截图失败')
                                requests.post(self.submit_url, headers=self.headers, data=json.dumps(body))
                        # 实时
                        if text['TypeCode'] == 'JQHOT_0100':
                            b = WeiBoScreenShot.time_screen_hot(self, text['Keyword'], text['Content'])
                            if b:
                                body['PicStr'] = json.dumps(b)
                                body['Message'] = '成功'
                                requests.post(self.submit_url, headers=self.headers, data=json.dumps(body))
                                print('实时提交一条任务')
                            else:
                                body['Message'] = '截图失败'
                                print('实时截图失败')
                                requests.post(self.submit_url, headers=self.headers, data=json.dumps(body))
                            pass
                    else:
                        print('状态码: %s' % re.status_code)
                    pass
                except Exception as e:
                    print(e)
                    WeiBoScreenShot.open_app_ready(self)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    xhs = WeiBoScreenShot()
    xhs.execute()

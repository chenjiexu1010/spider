# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import uiautomator2 as u2
import time
import uuid
import os
import requests
import json

'''
    微博 9.11.2
'''

# d = u2.connect_usb('c3cf4911')
package_name = 'com.sina.weibo'

d = u2.connect('0.0.0.0')


class WeiBoNewScreenShot(object):
    def __init__(self):
        # 需要保持屏幕常亮
        d.screen_on()
        # 注册监听事件
        d.set_new_command_timeout(300000)
        d.watcher("ALERT").when(text="不了，谢谢").click()
        d.watcher("ALERT").when(text="以后再说").click()
        self.get_url = 'http://222.185.251.62:22027/api/GetWeiBoShotData'
        self.submit_url = 'http://222.185.251.62:22027/api/PostWeiBoShotData'
        self.headers = {'Content-Type': 'application/json'}
        # 打开App
        d.app_start(package_name, launch_timeout=10)
        time.sleep(5)
        find = WeiBoNewScreenShot.init_page(self)
        if not find:
            print('未寻找到发现按钮')
            d.session(package_name)
            time.sleep(2)
            WeiBoNewScreenShot.__init__(self)

    # 重新启动微博
    def reset_weibo(self):
        d.session(package_name, launch_timeout=10)
        time.sleep(10)

    # 初始化页面
    def init_page(self):
        for i in range(1, 5):
            if d(description='发现').exists():
                return True
            else:
                d.press('back')
                time.sleep(2)
        return False

    # 关键词搜索
    def seach_key_world(self, key_word):
        d.screen_on()
        try:
            if not d(description='发现').exists():
                WeiBoNewScreenShot.reset_weibo(self)
                return False
            d(description='发现').click()
            d(className='android.widget.EditText').click()
            time.sleep(5)
            d(className='android.widget.EditText').send_keys(key_word)
            # 点击输入法搜索
            d.click(0.929, 0.954)
            time.sleep(5)
            return True
        except Exception as e:
            print(e)

    # 判断截图页面
    def judge_screen_page(self):
        if d(text='主页').exists() or d(text='微博正文').exists():
            return False
        if not d(className="android.view.ViewGroup").sibling(text="讨论").exists():
            return False
        return True

    # 图片转字节
    def pic_to_byte(self, pic_name):
        b = []
        with open(pic_name, 'rb') as f:
            for i in f.read():
                b.append(i)
        return b

    # 热门截图
    def hot_screen_hot(self, search_key, search_content):
        try:
            if not WeiBoNewScreenShot.seach_key_world(self, search_key):
                print('搜索关键词: %s' % search_key)
                return ''
            i = 0
            while True:
                if i >= 15:
                    d.press('back')
                    break
                # 找到热门版面
                if d(text='热门').exists():
                    i += 1
                    hot_info = d(text='热门').info
                    left = hot_info['bounds']['left']
                    top = hot_info['bounds']['top']
                    # 移动到热门版面
                    d(text="热门").gesture((left, top),
                                         (left, top),
                                         (0, 287), (0, 287))
                    time.sleep(3)
                    info = d(resourceId='com.sina.weibo:id/contentTextView').info
                    if search_content in info['contentDescription']:
                        # 判断移动位置后截图是否在准确位置
                        is_sure = WeiBoNewScreenShot.judge_screen_page(self)
                        if is_sure:
                            # 进入个人主页,判断微博昵称是否一致

                            pic_name = str(uuid.uuid1()) + '.png'
                            d.screenshot(pic_name)
                            # TODO 上传图片到图片服务器
                            res = WeiBoNewScreenShot.pic_to_byte(self, pic_name)
                            # 删除本地文件
                            os.remove(pic_name)
                            d.press('back')
                            print('热门截图成功 %s' % search_key)
                            return res
                    else:
                        # 内容不匹配 下移
                        d.swipe_ext('up', scale=0.3)
                        time.sleep(2)
                else:
                    i += 1
                    d.swipe_ext('up', scale=0.3)
                    time.sleep(2)
            pass
        except Exception as e:
            print(e)
        return ''

    # 实时截图
    def time_screen_hot(self, search_key, search_content):
        blog = ''
        res = ''
        if not WeiBoNewScreenShot.seach_key_world(self, search_key):
            print('搜索关键词: %s' % search_key)
            return ''
        i = 0
        while True:
            if i >= 20:
                break
            is_exists = d(text='实时微博').exists()
            if not is_exists:
                # 下移搜索
                d.swipe_ext('up', scale=0.3)
                time.sleep(2)
                continue
            # 找到实时微博版本d
            else:
                realtime_info = d(text='实时微博').info
                left = realtime_info['bounds']['left']
                top = realtime_info['bounds']['top']
                # 置顶实时版面
                d(text='实时微博').gesture((left, top),
                                       (left, top),
                                       (0, 287), (0, 287))
                time.sleep(2)
                while True:
                    try:
                        if i >= 20:
                            print('搜索达到上限')
                            d.press('back')
                            break
                        # 获取节点详细信息
                        blog_exists = d(resourceId='com.sina.weibo:id/contentTextView').exists()
                        if not blog_exists:
                            d.swipe_ext('up', scale=0.3)
                        info = d(resourceId='com.sina.weibo:id/contentTextView').info
                        if blog in info['contentDescription'] and blog.strip() != '':
                            # 下滑
                            d.swipe_ext('up', scale=0.3)
                            time.sleep(1)
                            i += 1
                            continue
                        else:
                            blog = info['contentDescription']
                        i += 1
                        # 找到不同博文 search_content in info['contentDescription']
                        if search_content in info['contentDescription']:
                            left = info['bounds']['left']
                            top = info['bounds']['top']
                            d(resourceId='com.sina.weibo:id/contentTextView').gesture(
                                (left, top),
                                (left, top),
                                (0, 459),
                                (0, 459))
                            time.sleep(5)
                            # TODO 截图
                            is_true = WeiBoNewScreenShot.judge_screen_page(self)
                            if is_true:
                                pic_name = str(uuid.uuid1()) + '.jpg'
                                d.screenshot(pic_name)
                                # TODO 上传图片到图片服务器
                                res = WeiBoNewScreenShot.pic_to_byte(self, pic_name)
                                # 删除本地文件
                                os.remove(pic_name)
                                d.press('back')
                                print('实时截图成功 %s' % search_key)
                                return res
                            else:
                                pass
                        else:
                            blog = info['contentDescription']
                            d.swipe_ext('up', scale=0.3)
                            time.sleep(1)
                    except Exception as e:
                        print(str(e))
        return res

    # 判断首页
    def judge_home(self):
        for i in range(1, 5):
            if d(description='发现').exists():
                return
            else:
                d.press('back')
                time.sleep(2)
        pass

    # 执行
    def execute(self):
        try:
            while True:
                try:
                    d.screen_on()
                    WeiBoNewScreenShot.judge_home(self)
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
                            d.healthcheck()
                            WeiBoNewScreenShot.reset_weibo(self)
                            # 等待qpy3运行
                            d.app_wait('com.hipipal.qpy3')
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
                            b = WeiBoNewScreenShot.hot_screen_hot(self, text['Keyword'], text['Content'])
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
                            b = WeiBoNewScreenShot.time_screen_hot(self, text['Keyword'], text['Content'])
                            if b:
                                body['PicStr'] = json.dumps(b)
                                body['Message'] = '成功'
                                requests.post(self.submit_url, headers=self.headers, data=json.dumps(body))
                                print('实时提交一条任务')
                            else:
                                body['Message'] = '截图失败'
                                print('实时截图失败')
                                requests.post(self.submit_url, headers=self.headers, data=json.dumps(body))
                    else:
                        print('状态码: %s' % re.status_code)
                    pass
                except Exception as e:
                    print(e)
                    WeiBoNewScreenShot.reset_weibo(self)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    weibo = WeiBoNewScreenShot()
    weibo.execute()
    pass

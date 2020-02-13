# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import uiautomator2 as u2
import time
import uuid
import os
import requests
import json

# 图片标记处理
pic_handle_insert_url = 'http://222.185.251.62:22027/api/phone/pichandle'
pic_change_url = 'http://222.185.251.62:22027/api/phone/getpicurl'

# pic_handle_insert_url = 'http://localhost:22027/api/phone/pichandle'
# pic_change_url = 'http://localhost:22027/api/phone/getpicurl'

# 获取截图任务url
# get_task_url = 'http://localhost:22027/api/redbook/gethotcommenttask'
# rb_hot_submit_url = 'http://localhost:22027/api/redbook/submithotcomment'
get_task_url = 'http://222.185.251.62:22027/api/redbook/gethotcommenttask'
rb_hot_submit_url = 'http://222.185.251.62:22027/api/redbook/submithotcomment'

# App包名
package_name = 'com.xingin.xhs'
qpy_package_name = 'com.hipipal.qpy3'

# 更新手机状态
update_phone_url = 'http://222.185.251.62:22027/api/phone/updatephoneinfo'


class RbHotCommentScreenShot(object):
    def __init__(self):
        self.device = u2.connect_usb('c2a948df')
        # self.device = u2.connect('0.0.0.0')
        self.device.set_new_command_timeout(300000)
        self.headers = {'Content-Type': 'application/json',
                        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36'}
        self.location = {}
        self.phonecode = '小米手机315'
        self.typecode = '小红书热评'
        self.b = []
        # RbHotCommentScreenShot.watcher_event(self)
        RbHotCommentScreenShot.open_app(self)

    # 更新手机信息
    def update_phone(self, typecode, logtype, phone_code):
        body = {
            "PhoneCode": phone_code,
            "TypeCode": typecode,
            "Message": "检测",
            "LogType": logtype
        }
        requests.post(update_phone_url, headers=self.headers, data=json.dumps(body))

    # TODO 注册监听事件 手机无法解析xml
    def watcher_event(self):
        self.device.watcher.when("跳过").click()
        self.device.watcher.when("取消").click()
        self.device.watcher.when("下次再说").click()
        self.device.watcher.when("知道了").click()
        self.device.watcher.when("暂时不用").click()
        self.device.watcher.start()
        self.device.watcher.start(5.0)
        # self.device.watcher("ALERT").when(text="跳过").click()
        # self.device.watcher("ALERT").when(text="取消").click()
        # self.device.watcher("ALERT").when(text="下次再说").click()
        # self.device.watcher("ALERT").when(text="知道了").click()
        # self.device.watcher("ALERT").when(text="暂时不用").click()

    def watcher_event2(self):
        if self.device(text='跳过').exists():
            self.device(text='跳过').click()
        if self.device(text='取消').exists():
            self.device(text='取消').click()
        if self.device(text='下次再说').exists():
            self.device(text='下次再说').click()
        if self.device(text='知道了').exists():
            self.device(text='知道了').click()
        if self.device(text='暂时不用').exists():
            self.device(text='暂时不用').click()
        if self.device(text='同意').exists():
            self.device(text='同意').click()

    # 打开小红书
    def open_app(self):
        self.device.app_start(package_name)
        time.sleep(5)
        while True:
            RbHotCommentScreenShot.watcher_event2(self)
            if self.device(text='首页').exists():
                break
            self.device.press('back')
            time.sleep(2)

    # 打开qpy
    def open_qpy_app(self):
        self.device.app_start(qpy_package_name)
        RbHotCommentScreenShot.watcher_event2(self)
        time.sleep(2)

    # 返回首页
    def back_to_home(self):
        for i in range(0, 5):
            if self.device(text='首页').exists():
                break
            else:
                RbHotCommentScreenShot.watcher_event2(self)
                self.device.press("back")
                time.sleep(2)

    # 搜索指定笔记
    def search_note(self, keyword, nickname, title, comment_content):
        '''
        :param keyword: 关键词
        :param nickname: 小红书昵称
        :param title: 笔记标题
        :param comment_content: 评论内容
        :return:错误信息 没有则为空字符串
        '''

        infor = ''
        self.b = []
        set_list = set()
        set_list2 = set()
        text = ''
        try:
            RbHotCommentScreenShot.back_to_home(self)
            if not self.device(resourceId='com.xingin.xhs:id/b_2').exists():
                infor = '首页搜索框获取失败'
                return infor
            self.device(resourceId='com.xingin.xhs:id/b_2').click()
            time.sleep(2)
            if not self.device(className='android.widget.EditText').exists():
                infor = '输入框获取失败'
                return infor
            self.device(className='android.widget.EditText').send_keys(keyword)
            self.device(text='搜索').click()
            time.sleep(2)
            while True:
                if self.device(text='- THE END -').exists():
                    infor = '笔记搜索完成'
                    return infor
                if len(set_list) > 30 or len(set_list2) > 30:
                    infor = '搜索达到上限'
                    break
                if title:
                    for head in self.device(resourceId='com.xingin.xhs:id/b96'):
                        # 标题
                        set_list.add(head.info['text'])
                        if title in head.info['text']:
                            text = head.info['text']
                            break
                if text:
                    break
                if nickname:
                    for nick in self.device(resourceId='com.xingin.xhs:id/b98'):
                        set_list2.add(nick.info['text'])
                        if nickname in nick.info['text']:
                            text = nick.info['text']
                            break
                if text:
                    break
                else:
                    # 下移
                    self.device.swipe_ext('up', scale=0.2)
                    time.sleep(1)
            if not text:
                infor = '搜索达到上限'
                return infor
            self.device(text=text).click()
            time.sleep(2)
            # 进入笔记操作
            self.b = RbHotCommentScreenShot.find_comment(self, comment_content)
            # 执行完毕返回首页
            RbHotCommentScreenShot.back_to_home(self)
        except Exception as e:
            pass
        return infor

    # 搜索指定评论
    def find_comment(self, comment):
        '''
        :param comment: 评论内容
        :return:返回图片数组 并且给location赋值
        '''
        try:
            self.location = {}
            # 判断是否在评论页面
            if not self.device(text='说点什么…').exists():
                return ''
            # 判断是否是视频
            if self.device(resourceId='com.xingin.xhs:id/xx').exists():
                self.device(resourceId='com.xingin.xhs:id/xx').click()
                time.sleep(1)
                for item in range(5):
                    for info in self.device(resourceId='com.xingin.xhs:id/crz'):
                        if comment in info.info['text']:
                            self.location = info.info
                            name = str(uuid.uuid1()) + '.png'
                            self.device.screenshot(name)
                            b = RbHotCommentScreenShot.pic_to_byte(self, name)
                            os.remove(name)
                            return b
                    self.device.swipe_ext('up', scale=0.2)
                    time.sleep(1)
            else:
                # 不是视频
                while True:
                    self.device.swipe_ext('up', scale=0.2)
                    time.sleep(1)
                    # 是否存在举报
                    if self.device(text='举报').exists():
                        self.device(text="举报").drag_to(171, 171, duration=0.5)
                        break
                for item in range(5):
                    for info in self.device(resourceId='com.xingin.xhs:id/crz'):
                        if comment in info.info['text']:
                            self.location = info.info
                            name = str(uuid.uuid1()) + '.png'
                            self.device.screenshot(name)
                            b = RbHotCommentScreenShot.pic_to_byte(self, name)
                            os.remove(name)
                            return b
                    self.device.swipe_ext('up', scale=0.2)
                    time.sleep(1)
        except Exception as e:
            RbHotCommentScreenShot.watcher_event2(self)
        return ''

    # 图片转字节
    def pic_to_byte(self, pic_name):
        b = []
        with open(pic_name, 'rb') as f:
            for i in f.read():
                b.append(i)
        return b

    def execute(self):
        while True:
            try:
                self.device.screen_on()
                RbHotCommentScreenShot.watcher_event2(self)
                # 获取任务
                re = requests.post(get_task_url, headers=self.headers)
                # 请求不成功 or 获取任务为空
                if re.status_code != 200 or not re.text:
                    RbHotCommentScreenShot.update_phone(self, self.typecode, '任务为空', self.phonecode)
                    time.sleep(10)
                    continue
                text = json.loads(re.text)
                text = json.loads(text)
                if text['Id'] == 0:
                    RbHotCommentScreenShot.update_phone(self, self.typecode, '任务为空', self.phonecode)
                    time.sleep(10)
                    continue
                str2 = RbHotCommentScreenShot.search_note(self, text['KeyWord'], text['NickName'], text['Title'],
                                                          text['CommentContent'])
                # 截图失败
                if not self.location or not self.b:
                    body = {
                        'LogId': text['Id'],
                        'Pic': ''
                    }
                    # 提交重置任务
                    requests.post(rb_hot_submit_url, headers=self.headers, data=json.dumps(body))
                    RbHotCommentScreenShot.update_phone(self, self.typecode, str2, self.phonecode)
                    continue
                body = {
                    'PicStr': json.dumps(self.b)
                }
                req = requests.post(pic_change_url, headers=self.headers, data=json.dumps(body))
                if req.status_code != 200:
                    RbHotCommentScreenShot.update_phone(self, self.typecode, '图片url获取失败', self.phonecode)
                    continue
                    # 生成url
                url = json.loads(req.text)
                handle_pic_body = {
                    'TaskId': text['TaskId'],
                    'LogId': text['Id'],
                    'TypeCode': 'JQHOT_0202',
                    'Left': self.location['bounds']['left'],
                    'LeftTop': self.location['bounds']['top'],
                    'Right': self.location['bounds']['right'],
                    'RightBottom': self.location['bounds']['bottom'],
                    'PicUrl': url,
                    'Message': '',  # 排名
                    'WorkTime': '',
                    'FinishTime': '',
                    'CreateTime': '',
                    'ReMark': '',
                    'Status': '0'
                }
                req = requests.post(pic_handle_insert_url, headers=self.headers,
                                    data=json.dumps(handle_pic_body))
            except Exception as e:
                RbHotCommentScreenShot.update_phone(self, self.typecode, str(e), self.phonecode)


if __name__ == '__main__':
    hot_comment = RbHotCommentScreenShot()
    # hot_comment.search_note('海外婚礼', '芝心全球旅行婚礼', '3️⃣万元如何办一场海外婚礼，低成本旅行结婚', '毛里求斯婚礼有做吗 2019-06-29')
    hot_comment.execute()

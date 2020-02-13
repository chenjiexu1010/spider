import uiautomator2 as u2
import time
import json
import uuid
import os
import requests

# 图片标记处理
pic_handle_insert_url = 'http://222.185.251.62:22027/api/phone/pichandle'
pic_change_url = 'http://222.185.251.62:22027/api/phone/getpicurl'
get_task = 'http://222.185.251.62:22027/api/GetWeiBoDropDownAccountData'


class WeiBoDropAccount(object):
    def __init__(self):
        # 手机远程连接Ip
        self.device = u2.connect('0.0.0.0')
        # self.device = u2.connect_usb('33c34c6f')
        self.package = 'com.sina.weibo'
        self.headers = {'Content-Type': 'application/json'}
        self.b = []
        self.location = {}
        WeiBoDropAccount.open_app(self)

    # 打开App
    def open_app(self):
        self.device.app_start(self.package, wait=True)
        for i in range(5):
            if not self.device(description='发现').exists():
                self.device.press('back')
                time.sleep(1)
            else:
                break
        time.sleep(5)

    def come_back(self):
        for i in range(5):
            if not self.device(description='发现').exists():
                self.device.press('back')
                time.sleep(1)
            else:
                break

    # 执行主体
    def search_account(self, keyword, nickname):
        info = ''
        self.location = {}
        self.b = []
        try:
            # 返回发现
            if not self.device(description='发现').exists():
                info = '微博:发现按钮寻找失败'
                return info
            self.device(description='发现').click()
            if not self.device(className='android.widget.EditText').exists():
                info = '微博:搜索输入框不存在'
                return info
            self.device(className='android.widget.ViewFlipper').click()
            self.device(className='android.widget.EditText').send_keys(keyword)
            self.device.click(0.938, 0.624)
            for account_info in self.device(className='android.widget.TextView'):
                if nickname in account_info.info['text']:
                    name = str(uuid.uuid1()) + '.png'
                    self.location = account_info.info
                    self.device.screenshot(name)
                    self.b = WeiBoDropAccount.pic_to_byte(self, name)
                    os.remove(name)
                    return info
            return info
        except Exception as e:
            print(e)

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
                # 获取任务
                re = requests.post(get_task, headers=self.headers)
                # 请求不成功 or 获取任务为空
                if re.status_code != 200 or not re.text:
                    time.sleep(10)
                    continue
                text = json.loads(re.text)
                str2 = WeiBoDropAccount.search_account(self, text['Keyword'],
                                                       text['NickName'])
                # 截图失败
                if not self.location or not self.b:
                    continue
                body = {
                    'PicStr': json.dumps(self.b)
                }
                req = requests.post(pic_change_url, headers=self.headers, data=json.dumps(body))
                if req.status_code != 200:
                    continue
                url = json.loads(req.text)
                handle_pic_body = {
                    'TaskId': text['TaskId'],
                    'LogId': text['LogId'],
                    'TypeCode': 'JQHOT_0106',
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
                print(e)


if __name__ == '__main__':
    weibo = WeiBoDropAccount()
    # weibo.search_account('王源', 'TFBOYS-王源 ')
    weibo.execute()

# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import requests
import logging
from requests.auth import HTTPProxyAuth
import json
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import uuid
import os
from flask import Flask

host = '192.168.2.74'
app = Flask(__name__)
# logging
fh = logging.FileHandler('log.log')
fh.setLevel(logging.DEBUG)
fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
datefmt = "%a %d %b %Y %H:%M:%S"
formatter = logging.Formatter(fmt, datefmt)
fh.setFormatter(formatter)


class WeiBoShot(object):
    def __init__(self):
        self.option = Options()
        self.option.add_argument('--headless')
        self.option.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=self.option)
        self.driver.set_script_timeout(1)
        self.open_html_url = 'http://localhost:63342/Jeqee热门/spider/weibo/微博Com截图(代理)/weibocom_shot/'
        self.auth = HTTPProxyAuth('xxx', 'xxx')
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
        # 初始化日志
        self.logger = logging.getLogger('weibo_com')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(fh)

    def get_proxy_ip(self):
        ip = ''
        try:
            proxy_result = requests.get('http://192.168.2.74:25003/api/GetRandomProxy')
            if proxy_result.status_code == 200:
                info = json.loads(proxy_result.content.decode('utf-8'))
                ip = info['_ProxyAddress']
        except Exception as e:
            self.logger.error(str(e))
            return ip

    def download_element(self, key_world, mid):
        try:
            ip = WeiBoShot.get_proxy_ip(self)
            if not ip:
                self.logger.warning('代理获取失败')
                return json.dumps({'message': '代理获取失败', 'screen': ''})
            page_result = requests.get('https://s.weibo.com/weibo?q=%s&Refer=SWeibo_box' % key_world,
                                       proxies={'http': ip},
                                       headers=self.headers, auth=self.auth)
            if not page_result.status_code == 200:
                self.logger.warning('请求返回状态码不为200: %d' % page_result.status_code)
                return json.dumps({'message': '请求返回:' + page_result.status_code, '截图': ''})
            file_name = str(uuid.uuid1()) + '.html'
            result = page_result.content
            # 保存html元素
            with open(file_name, 'wb') as f:
                f.write(result)
            # TODO 查找 mid
            pic_byte_arr = WeiBoShot.find_mid(self, mid, file_name)
            if pic_byte_arr:
                self.logger.info('截图成功 Keyword: %s Mid: %s' % (key_world, mid))
                return json.dumps({'message': '截图成功', 'screen': json.dumps(pic_byte_arr)})
            self.logger.warning('截图失败 Keyword: %s Mid: %s' % (key_world, mid))
            return json.dumps({'message': '截图失败', 'screen': ''})
        except Exception as e:
            print(e)

    def find_mid(self, mid, file_name):
        pic_byte = []
        # 随机pic_name
        pic_name = str(uuid.uuid1()) + '.png'
        try:
            # 打开本地静态文件
            self.driver.get(self.open_html_url + file_name)
            mid_elements = self.driver.find_elements_by_xpath('//div[@mid]')
            if not mid_elements:
                self.logger.warning('mid元素获取为空mid: %s' % mid)
                return pic_byte
            for i in range(0, mid_elements.__len__()):
                # if i == 0:
                #     continue
                if mid in mid_elements[i].get_attribute('mid'):
                    try:
                        self.driver.execute_async_script(
                            "document.getElementsByClassName('card-wrap')[%d].style.border = '2px solid red'" % i)
                    except Exception as ex:
                        try:
                            self.driver.execute_async_script(
                                "window.scrollTo(0, %d)" % mid_elements[i].location['y'])
                        except Exception as ex2:
                            pass
                    # 设置浏览器高度
                    self.driver.set_window_size(width=800, height=800 + mid_elements[i].location['y'])
                    try:
                        self.driver.execute_async_script(
                            "window.scrollTo(0, 0)")
                    except Exception as ex3:
                        pass
                    self.driver.save_screenshot(pic_name)
                    print('成功截到图mid:' + mid)
                    # 返回字节数组
                    pic_byte = WeiBoShot.pic_to_byte(pic_name)
                    break
        except Exception as e:
            print(e)
        finally:
            # 删除本地 html文件 以及图片
            if pic_name:
                os.remove(pic_name)
            if file_name:
                os.remove(file_name)
            self.logger.info('删除本地文件成功PicName: %s ,FileName: %s' % (pic_name, file_name))
            return pic_byte

    @staticmethod
    def pic_to_byte(pic_name):
        b = []
        with open(pic_name, 'rb') as f:
            for i in f.read():
                b.append(i)
        return b


weibo = WeiBoShot()


# com截图
@app.route('/comscreenshot/<keyword>/<mid>')
def com_hot_screen(keyword, mid):
    if not keyword or not mid:
        return '关键参数不能为空'
    return weibo.download_element(key_world=keyword, mid=mid)


if __name__ == '__main__':
    app.run(host=host, port=5001)

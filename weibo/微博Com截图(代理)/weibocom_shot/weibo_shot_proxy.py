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
import time

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
        self.driver.set_page_load_timeout(10)
        # 通用文件夹\python打包\微博com无账号截图\dist
        # self.open_html_url = 'http://localhost:63342/Jeqee热门/spider/weibo/微博Com截图(代理)/weibocom_shot/exe文件/dist/'
        self.open_html_url = 'http://localhost:63342/Jeqee热门/spider/weibo/微博Com截图(代理)/weibocom_shot/'
        self.auth = HTTPProxyAuth('jeqee', 'jeqeeproxy')
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'Host': 's.weibo.com'}
        self.has_cookie_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'Host': 's.weibo.com',
            'Cookie': 'SINAGLOBAL=2079748157535.4148.1562656336661; _s_tentry=-; Apache=6138501991200.746.1578878421920; ULV=1578878421977:15:2:1:6138501991200.746.1578878421920:1577966277068; login_sid_t=4041ea8280741ef6a60c24968bf7ed52; cross_origin_proto=SSL; WBtopGlobal_register_version=307744aa77dd5677; secsys_id=d3e0da3cb4c0fb539669ba32cf3d0751; ALF=1610614524; SSOLoginState=1579078525; SCF=AncjsCf7zbAbUzNBAKOizieYzy1LkJJc5eum43dQUuxtx1pHo_67XdOiZfYQ5pr9nZip8tM5XaA6dshnDiGWE1s.; SUB=_2A25zGqMmDeRhGeRG4loZ8S_LzTmIHXVQUZPurDV8PUNbmtAfLU7mkW9NTeZINGNGUkBCRAcmRLrsnuAuL4q2BGyT; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFOfqD9fkE8ALcVFJfdDIpl5JpX5KzhUgL.FozR1KnReK2NSo-2dJLoIfQLxK-L12qL1KqLxKBLBonLB-2LxK-L1K5L12BLxK-LB-BL1KMLxKBLBo.L1-qLxK-LB.-L1hnLxK.L1-2LB.-LxK-L1K-L122LxKqL1hnL1K2LxK-L12-LB.zt; SUHB=0S7yje5GVwlj4F; wvr=6; UOR=,,v3.jqsocial.com; webim_unReadCount=%7B%22time%22%3A1579140897294%2C%22dm_pub_total%22%3A5%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A43%2C%22msgbox%22%3A0%7D; WBStorage=42212210b087ca50|undefined'
        }
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

    def download_element(self, key_world, mid, type_code):
        try:
            ip = WeiBoShot.get_proxy_ip(self)
            if not ip:
                self.logger.warning('代理获取失败')
                return '代理获取失败'
            page_result = requests.get('https://s.weibo.com/weibo?q=%s&Refer=SWeibo_box' % key_world,
                                       proxies={'http': ip},
                                       headers=self.headers, auth=self.auth)
            if not page_result.status_code == 200:
                self.logger.warning('失败请求返回状态码不为200: %d' % page_result.status_code)
                return '请求返回状态码不为200: %d' % page_result.status_code
            file_name = str(uuid.uuid1()) + '.html'
            result = page_result.content
            # 保存html元素到本地
            with open(file_name, 'wb') as f:
                f.write(result)
            # 根据mid搜索对应博文
            pic_byte_arr = WeiBoShot.find_mid(self, mid, file_name, type_code)
            if pic_byte_arr:
                # 截图成功
                self.logger.info('截图成功 Keyword: %s Mid: %s' % (key_world, mid))
                return json.dumps(pic_byte_arr)
            # 截图失败
            self.logger.warning('截图失败 Keyword: %s Mid: %s' % (key_world, mid))
            return '失败 Keyword: %s Mid: %s' % (key_world, mid)
        except Exception as e:
            self.logger.error(str(e))
        finally:
            self.driver.quit()
        return '失败'

    # TODO  携带Cookie请求搜索页面
    def download_element_with_cookie(self, key_world, mid, type_code):
        try:
            # ip = WeiBoShot.get_proxy_ip(self)
            # if not ip:
            #     self.logger.warning('代理获取失败')
            #     return '代理获取失败'
            page_result = requests.get('https://s.weibo.com/weibo?q=%s&Refer=SWeibo_box' % key_world,
                                       headers=self.has_cookie_headers)
            if not page_result.status_code == 200:
                self.logger.warning('请求返回状态码不为200: %d' % page_result.status_code)
                return '请求返回状态码不为200: %d' % page_result.status_code
            file_name = str(uuid.uuid1()) + '.html'
            result = page_result.content
            # 保存html元素到本地
            with open(file_name, 'wb') as f:
                f.write(result)
            # 根据mid搜索对应博文
            pic_byte_arr = WeiBoShot.find_mid(self, mid, file_name, type)
            if pic_byte_arr:
                # 截图成功
                self.logger.info('截图成功 Keyword: %s Mid: %s' % (key_world, mid))
                return json.dumps(pic_byte_arr)
            # 截图失败
            self.logger.warning('截图失败 Keyword: %s Mid: %s' % (key_world, mid))
            return ''
        except Exception as e:
            self.logger.error(str(e))
        return ''

    def find_mid(self, mid, file_name, type_code):
        pic_byte = []
        pic_name = ''
        try:
            # TODO 打开获取元素为空  打开本地静态文件
            self.driver.get(self.open_html_url + file_name)
            time.sleep(2)
            card_elements = self.driver.find_elements_by_class_name('card-wrap')
            if not card_elements:
                self.logger.warning('card元素获取失败 mid %s' % mid)
                return pic_byte
            for i in range(0, card_elements.__len__()):
                # if i == 0:
                #     continue
                check_find = card_elements[i].get_attribute('mid')
                if not check_find:
                    self.logger.warning('当前card不存在mid属性 mid: %s' % mid)
                    continue
                if mid in check_find:
                    self.driver.execute_script(
                        "document.getElementsByClassName('card-wrap')[%d].style.border = '2px solid red'" % (
                            i))
                    # # 热门  实时 状态区分
                    # if type_code == 0 and '热门' in card_elements[i].text[0:20].strip():
                    #     self.driver.execute_async_script(
                    #         "document.getElementsByClassName('card-wrap')[%d].style.border = '2px solid red'" % (
                    #             i))
                    # else:
                    #     return pic_byte
                    # if type_code == 1:
                    #     self.driver.execute_async_script(
                    #         "document.getElementsByClassName('card-wrap')[%d].style.border = '2px solid red'" % (
                    #             i))
                    self.driver.execute_script(
                        "window.scrollTo(0, %d)" % card_elements[i].location['y'])
                    self.driver.set_window_size(width=800, height=800 + card_elements[i].location['y'])
                    self.driver.execute_script("window.scrollTo(0, 0)")
                    pic_name = str(uuid.uuid1()) + '.png'
                    self.driver.save_screenshot(pic_name)
                    print('成功截到图mid:' + mid)
                    # 返回字节数组
                    pic_byte = WeiBoShot.pic_to_byte(pic_name)
                    return pic_byte
        except Exception as e:
            print(e)
        finally:
            # 删除本地 html文件 以及图片
            if pic_name and pic_name != '':
                os.remove(pic_name)
            if file_name and file_name != '':
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


@app.route('/comscreenshot/<keyword>/<mid>/<int:type_code>')
def com_hot_screen(keyword, mid, type_code):
    # TODO 占用内存
    wei_bo = WeiBoShot()
    if not keyword or not mid:
        return '关键参数不能为空'
    # 0 热门   1 实时
    res = wei_bo.download_element(key_world=keyword, mid=mid, type_code=type_code)
    if res:
        return res
    return '截图失败'


# @app.route('/comscreenshotwithcookie/<keyword>/<mid>')
# def com_hot_screen(keyword, mid):
#     if not keyword or not mid:
#         return '关键参数不能为空'
#     res = weibo.download_element_with_cookie(key_world=keyword, mid=mid)
#     if res:
#         return jsonify(res)
#     return '截图失败'


if __name__ == '__main__':
    app.run(host=host, port=5001)
    # wei_bo = WeiBoShot()
    # wei_bo.download_element('手表', '', 0)
    # wei_bo.download_element_with_cookie('海外婚礼', '')

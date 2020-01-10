# -*- coding:utf-8 -*-
# !/usr/bin/Python3
from bs4 import BeautifulSoup
from bs4 import Tag
import requests
from flask import Flask
import json
from requests.auth import HTTPProxyAuth
import datetime

# https://s.weibo.com/weibo?q=婚纱&Refer=SWeibo_box

host = '192.168.2.74'
app = Flask(__name__)

# 获取代理url
proxy_url = 'http://192.168.2.74:25003/api/GetRandomProxy'
ProxyUsername = "jeqee"
ProxyPassword = "jeqeeproxy"
# 代理授权
auth = HTTPProxyAuth(ProxyUsername, ProxyPassword)

'''
   查找检测码
      搜索检测码，获取 上级元素<p> 获取 <p> 的上级元素 
     1. <div>  class="content" node-type="like",
        (获取兄弟元素div class="avator" 获取href属性提取uid  //weibo.com/2276241027?refer_flag=1001030103_)
     2. 获取 div 上级元素 class="card-feed"
     3. 获取 div 上级元素 class="card"
     4. 获取 div 上级元素 class="card" <div class="card-wrap" action-type="feed_list_item" mid="4458823492362965">
        获取mid 
'''

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}


# 获取代理ip
def get_proxy_ip():
    ip = ''
    try:
        proxy_result = requests.get('http://192.168.2.74:25003/api/GetRandomProxy')
        if proxy_result.status_code == 200:
            info = json.loads(proxy_result.content.decode('utf-8'))
            ip = info['_ProxyAddress']
    except Exception as e:
        print('获取代理ip异常: %s' % str(e))
    return ip


# 纯文字匹配
def get_weibo_com_url(key_world, test_code):
    try:
        print('获取到任务 %s 关键词: %s,检测码:%s' % (datetime.datetime.now(), key_world, test_code))
        blog_list = []
        # 获取代理
        ip = get_proxy_ip()
        if not ip:
            return '代理ip获取失败'
        page_result = requests.get('https://s.weibo.com/weibo?q=%s&Refer=SWeibo_box' % key_world, proxies={'http': ip},
                                   headers=header, auth=auth)
        # 解析html文档
        if not page_result.status_code == 200:
            return blog_list
        soup = BeautifulSoup(page_result.content)
        # <class 'bs4.element.ResultSet'>
        elements = soup.find_all('p', attrs={"class": "txt"})
        for element in elements:
            uid = ''
            mid = ''
            # <class 'bs4.element.Tag'>
            for content in element.contents:
                print(content.string)
                # 匹配检测码
                if test_code in content:
                    # 获取当前元素的父元素
                    parent = element.parent
                    if parent is None:
                        return blog_list
                    get_uid_element = parent.contents[1]
                    if get_uid_element is None:
                        return blog_list
                    blog_url = get_uid_element.contents[3].contents[1].attrs['href']
                    # '//weibo.com/2276241027?refer_flag=1001030103_'
                    uid = blog_url.split("?")[0].split("/")[3]
                    # 获取mid
                    parent = parent.parent
                    if parent is None:
                        return blog_list
                    parent = parent.parent
                    if parent is None:
                        return blog_list
                    parent = parent.parent
                    if parent is None:
                        return blog_list
                    mid = parent.attrs['mid']
                    uid_mid = {'uid': uid, 'mid': mid}
                    blog_list.append(uid_mid)
                    break
        if blog_list:
            print('存在检测码:%s' % blog_list)
            return json.dumps(blog_list)
        return '返回数据为空'
    except Exception as e:
        return '程序异常' + str(e)


# 匹配末尾字符串
def get_weibo_com_end(key_world, test_code, type_code):
    try:
        print('获取到任务 %s 关键词: %s,检测码:%s' % (datetime.datetime.now(), key_world, test_code))
        blog_list = []
        # 获取代理
        ip = get_proxy_ip()
        if not ip:
            return '代理ip获取失败'
        page_result = requests.get('https://s.weibo.com/weibo?q=%s&Refer=SWeibo_box' % key_world, proxies={'http': ip},
                                   headers=header, auth=auth)
        # 解析html文档
        if not page_result.status_code == 200:
            return blog_list
        soup = BeautifulSoup(page_result.content)
        # <class 'bs4.element.ResultSet'>
        elements = soup.find_all('p', attrs={"class": "txt"})
        for element in elements:
            uid = ''
            mid = ''
            result = []
            # <class 'bs4.element.Tag'>
            for content in element.contents:
                if not isinstance(content, Tag) or not content:
                    result.append(content)
            if result:
                res = ''.join(result).strip().replace(' ', '')
                code = res[-15:-1]
                # 匹配检测码
                if test_code in code:
                    print('匹配到检测码:%s' % test_code)
                    parent = element.parent
                    if parent is None:
                        return blog_list
                    get_uid_element = parent.contents[1]
                    if get_uid_element is None:
                        return blog_list
                    blog_url = get_uid_element.contents[3].contents[1].attrs['href']
                    # '//weibo.com/2276241027?refer_flag=1001030103_'
                    uid = blog_url.split("?")[0].split("/")[3]
                    # 获取mid
                    parent = parent.parent
                    if parent is None:
                        return blog_list
                    parent = parent.parent
                    if parent is None:
                        return blog_list
                    parent = parent.parent
                    if parent is None:
                        return blog_list
                    is_real = True
                    for tag in parent.contents:
                        #  TODO 判断是否是热门 card-top 精选 或者 热门 检测
                        if isinstance(tag, Tag) and type_code == 0 and tag.get('class')[0] == 'card-top':
                            print('检测到热门 %s' % test_code)
                            mid = parent.attrs['mid']
                            uid_mid = {'uid': uid, 'mid': mid}
                            blog_list.append(uid_mid)
                            is_real = False
                            break
                    if type_code == 1 and is_real:
                        print('检测到实时 %s' % test_code)
                        # 实时截图
                        mid = parent.attrs['mid']
                        uid_mid = {'uid': uid, 'mid': mid}
                        blog_list.append(uid_mid)
                    break
            else:
                print('未匹配到检测码%s -- %s' % (result, test_code))
        if blog_list:
            print('存在检测码:%s' % blog_list)
            return json.dumps(blog_list)
        return '返回数据为空'
    except Exception as e:
        print('检测出现异常: %s' % str(e))




@app.route('/comshot/<keyword>/<code>')
def hot_screen(keyword, code):
    return get_weibo_com_url(keyword, code)


@app.route('/comshot2/<keyword>/<code>/<int:type_code>')
def com_hot_screen(keyword, code, type_code):
    return get_weibo_com_end(keyword, code, type_code)


if __name__ == '__main__':
    app.run(host=host, port=5000)
    # result = get_weibo_com_url('海外婚礼', '北上看到的冰川是你')
    # result2 = get_weibo_com_end('篮球', '1月10日。', 1)
    # print('执行结束' + result)

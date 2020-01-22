# -*- coding:utf-8 -*-
# !/usr/bin/Python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import redis
import time
from http.cookies import SimpleCookie


# 微博登录
class WeiBoLogin(object):
    def __init__(self):
        self.pool = redis.ConnectionPool(host='192.168.2.74')
        self.r = redis.Redis(connection_pool=self.pool)
        # 初始话selenium
        self.option = Options()
        self.account_list = []
        # self.option.add_argument('--headless')
        self.option.add_argument('--disable-gpu')
        self.option.add_argument('--ignore-certificate-errors')
        cookie = 'SINAGLOBAL=2079748157535.4148.1562656336661; _s_tentry=-; Apache=6138501991200.746.1578878421920; ULV=1578878421977:15:2:1:6138501991200.746.1578878421920:1577966277068; login_sid_t=4041ea8280741ef6a60c24968bf7ed52; cross_origin_proto=SSL; WBtopGlobal_register_version=307744aa77dd5677; secsys_id=d3e0da3cb4c0fb539669ba32cf3d0751; ALF=1610614524; SSOLoginState=1579078525; SCF=AncjsCf7zbAbUzNBAKOizieYzy1LkJJc5eum43dQUuxtx1pHo_67XdOiZfYQ5pr9nZip8tM5XaA6dshnDiGWE1s.; SUB=_2A25zGqMmDeRhGeRG4loZ8S_LzTmIHXVQUZPurDV8PUNbmtAfLU7mkW9NTeZINGNGUkBCRAcmRLrsnuAuL4q2BGyT; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFOfqD9fkE8ALcVFJfdDIpl5JpX5KzhUgL.FozR1KnReK2NSo-2dJLoIfQLxK-L12qL1KqLxKBLBonLB-2LxK-L1K5L12BLxK-LB-BL1KMLxKBLBo.L1-qLxK-LB.-L1hnLxK.L1-2LB.-LxK-L1K-L122LxKqL1hnL1K2LxK-L12-LB.zt; SUHB=0S7yje5GVwlj4F; wvr=6; UOR=,,v3.jqsocial.com; webim_unReadCount=%7B%22time%22%3A1579140897294%2C%22dm_pub_total%22%3A5%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A43%2C%22msgbox%22%3A0%7D; WBStorage=42212210b087ca50|undefined'
        cookies = SimpleCookie(cookie)
        self.driver = webdriver.Chrome(options=self.option)
        self.driver.add_cookie({i.key: i.value for i in cookies.values()})
        self.driver.set_script_timeout(1)
        # 页面加载超时时间
        self.driver.set_page_load_timeout(10)
        # 微博主页
        self.login_url = 'https://weibo.com/'

    def login(self, username, password):
        try:
            self.driver.get(self.login_url)
            time.sleep(10)
            login_button = self.driver.find_element_by_link_text('登录')
            # 点击登录
            login_button.click()
            username_element = self.driver.find_element_by_name('username')
            username_element.clear()
            username_element.send_keys(username)
            password_element = self.driver.find_element_by_name('password')
            password_element.clear()
            password_element.send_keys(password)
            sure_login = self.driver.find_element_by_link_text('登录')
            sure_login.click()
            # username_element = self.driver.find_element_by_name('username')
            # username_element.send_keys(username)
            # password_element = self.driver.find_element_by_name('password')
            # password_element.send_keys(password)
            # login_button = self.driver.find_element_by_class_name('W_btn_a btn_32px')
            # login_button.click()
        except Exception as e:
            print(e)

    def get_wei_bo_cookie(self):
        account_info = WeiBoLogin.get_wei_bo_account(self)
        if not account_info:
            print('获取账号失败')
            return
        account = account_info['account']
        password = account_info['password']
        print(type('获取到执行账号:%s 密码:%s' % (account, password)))
        # 登录
        WeiBoLogin.login(self, account, password)

    def load_account(self):
        with open('weiboaccount.txt', 'r', encoding='utf-8') as w:
            self.account_list = w.readlines()
        if not self.account_list:
            print('账号获取数量为空')
        print('获取到账号数量:%d' % self.account_list.__len__())

    def get_wei_bo_account(self):
        account_info = self.account_list[0]
        if account_info:
            account = account_info.split(' ')[0].strip()
            password = account_info.split(' ')[1].strip()
            cookie = self.r.get(account)
            # 存在cookie
            if not cookie:
                print('当前账号不存在Cookie:%s' % account)
                return {'account': account, 'password': password}
        print('未获取到可获取cookie的账号')
        return ''


if __name__ == '__main__':
    wei_bo_login = WeiBoLogin()
    wei_bo_login.load_account()
    wei_bo_login.get_wei_bo_cookie()
    pass

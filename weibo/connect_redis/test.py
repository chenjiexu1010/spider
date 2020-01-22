# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import redis
from selenium import webdriver
from http.cookies import SimpleCookie
from selenium.webdriver.chrome.options import Options

# 微博账号 绑定工作地 根据工作地获取IP 请求头中加入Cookie参数

# cookie = 'SINAGLOBAL=2079748157535.4148.1562656336661; _s_tentry=-; Apache=6138501991200.746.1578878421920; ULV=1578878421977:15:2:1:6138501991200.746.1578878421920:1577966277068; login_sid_t=4041ea8280741ef6a60c24968bf7ed52; cross_origin_proto=SSL; WBtopGlobal_register_version=307744aa77dd5677; secsys_id=d3e0da3cb4c0fb539669ba32cf3d0751; ALF=1610614524; SSOLoginState=1579078525; SCF=AncjsCf7zbAbUzNBAKOizieYzy1LkJJc5eum43dQUuxtx1pHo_67XdOiZfYQ5pr9nZip8tM5XaA6dshnDiGWE1s.; SUB=_2A25zGqMmDeRhGeRG4loZ8S_LzTmIHXVQUZPurDV8PUNbmtAfLU7mkW9NTeZINGNGUkBCRAcmRLrsnuAuL4q2BGyT; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFOfqD9fkE8ALcVFJfdDIpl5JpX5KzhUgL.FozR1KnReK2NSo-2dJLoIfQLxK-L12qL1KqLxKBLBonLB-2LxK-L1K5L12BLxK-LB-BL1KMLxKBLBo.L1-qLxK-LB.-L1hnLxK.L1-2LB.-LxK-L1K-L122LxKqL1hnL1K2LxK-L12-LB.zt; SUHB=0S7yje5GVwlj4F; wvr=6; UOR=,,v3.jqsocial.com; webim_unReadCount=%7B%22time%22%3A1579140897294%2C%22dm_pub_total%22%3A5%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A43%2C%22msgbox%22%3A0%7D; WBStorage=42212210b087ca50|undefined'
# cookies = SimpleCookie(cookie)
# print(type(cookies))
# for i in cookies.values():
#     print(i.key + ' ' + i.value)

option = Options()
option.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=option)
driver.get('https://s.weibo.com')
login_btn = driver.find_element_by_link_text('登录')
login_btn.click()
username_element = driver.find_element_by_name('username')
username_element.send_keys('etzticdzwaerw-arc821@yahoo.com')
password_element = driver.find_element_by_name('password')
password_element.send_keys('TJcgulgnhms54')
login = driver.find_element_by_class_name('W_btn_a btn_34px')
login.click()
cookies = driver.get_cookies()
print(cookies)

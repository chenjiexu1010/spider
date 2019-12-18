# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import time
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy

# 打开浏览器
options = webdriver.ChromeOptions()
# 设置无头浏览器
# options.add_argument('--headless')
# 禁用gpu
options.add_argument('--disable-gpu')
options.add_argument('--''')

browser = webdriver.Chrome(options=options, executable_path=r'E:\通用文件夹\chromedriver\chromedriver.exe')
browser.set_window_size(width=800, height=800)
browser.get('https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D' + '婚纱')

Proxy.add_to_capabilities()

# selenium.webdriver.common.proxy.Proxy(raw=None)[source]¶

# browser.back()
# 等待十秒加载
# browser.implicitly_wait(10)
time.sleep(5)

# cards = browser.find_elements_by_class_name('card')
# for title in cards:
#     print(title.text)

# 截图
# browser.save_screenshot('home.png')

# print(browser.page_source)

# browser.execute_script('return document.getElementsByClassName(\'card\')[0].remove()')

# browser.close()

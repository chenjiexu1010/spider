# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import psutil
import os
import time
import datetime
import threading

PROCESS_NAME = 'Jeqee.JqSocial.ExecuteTools.exe'
PROCESS_PATH = r'C:\V3微博拉私信\V3App拉私信\Jeqee.JqSocial.ExecuteTools.exe'
# PROCESS_PATH = r'D:\codes\V3\Client\Jeqee.JqSocial.ExecuteTools\bin\Debug\Jeqee.JqSocial.ExecuteTools.exe'
PROCESS_KILL = 'taskkill /f /t /im Jeqee.JqSocial.ExecuteTools.exe'
PERCENT = 90.0


def open_process():
    os.system(PROCESS_PATH)
    print('打开私信工具结束')


while True:
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        print('当前CPU使用率: %s   %s' % (cpu_percent, datetime.datetime.now()))
        if cpu_percent > PERCENT:
            print('检测到CPU使用率过高,即将关闭V3拉私信程序')
            os.system(PROCESS_KILL)
            print('V3拉私信已关闭')
            # todo os 打开微博拉私信工具会卡住不动 暂时用一个后台线程处理
            t = threading.Thread(target=open_process)
            t.setDaemon(True)
            t.start()
            # os.system(PROCESS_PATH)
            print('重启V3拉私信程序成功')
        time.sleep(30)
    except Exception as e:
        print(e)

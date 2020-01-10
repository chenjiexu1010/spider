# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import psutil
import os

'''
    process Jeqee.JqSocial.ExecuteTools.exe
    process_url = 'D:\codes\V3\Client\Jeqee.JqSocial.ExecuteTools\bin\Debug\Jeqee.JqSocial.ExecuteTools.exe'
    当前CPU使用率: 7.0   2019-12-24 15:09:45.456713
    当前CPU使用率: 13.8   2019-12-24 15:10:16.457830
'''

common = r'D:\codes\V3\Client\Jeqee.JqSocial.ExecuteTools\bin\Debug\Jeqee.JqSocial.ExecuteTools.exe'

cpu_count = psutil.cpu_count()
print('CPU数量: %s' % cpu_count)
percent = psutil.cpu_percent(interval=1)
print(str('CPU使用率:%s ' % percent + '%' + str(type(percent))))

# process = psutil.Process(15724)
# print(process.cpu_percent(1))

# for i in range(10):
#     print(psutil.cpu_percent(interval=1, percpu=True))

# 遍历进程名字
# pids = psutil.pids()
# for p in pids:
#     process = psutil.Process(p)
#     print(process.name())

# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import pymssql
import email.mime.text
import smtplib
import time
import datetime
import decimal

SERVER = '192.168.2.181'
USERNAME = 'chenjiexu'
PASSWORD = 'NHXoaVPJX8sIAgE3gdSu'

conn = pymssql.connect(SERVER, USERNAME, PASSWORD, 'Jeqee_V3_Clone')
cursor = conn.cursor()
SELECT_HOUR = 'SELECT vps,max(WorkTime) AS 最新拉取时间 from CloneLog where vps not in (\'微信克隆01\',\'微信克隆02\') and DATEDIFF(HOUR ,WorkTime,getdate()) <= 5 and LogType = \'上传朋友圈成功\' group by vps order by vps'

# 邮件发送方
msg_from = 'chenjiexu_1991@qq.com'
# 授权码
password = 'mkcirhcjxemmbehg'
# 收件人邮箱
msg_to = 'chenjiexu@jeqee.com'


class XiaoMiCheckTool(object):
    global mobiles

    def __init__(self):
        if not cursor:
            print('数据库连接失败')
        global mobiles
        # 初始化监听手机
        with open('MobilePhone.txt', 'r', encoding='utf8') as r:
            mobiles = list(map(lambda x: x.strip().replace('\ufeff', ''), r.readlines()))

    def send_email(self, content):
        if content:
            content = ','.join(content)
            subject = '微信手机克隆'
            msg = email.mime.text.MIMEText(content)
            msg['Subject'] = subject
            msg['From'] = msg_from
            msg['To'] = msg_to
            try:
                s = smtplib.SMTP_SSL('smtp.qq.com', 465)
                s.login(msg_from, password)  # 登陆QQ邮箱服务器
                s.sendmail(msg_from, msg_to, msg.as_string())  # 发送邮件
                print("邮件发送成功 %s " % (datetime.datetime.now()))
                s.quit()
            except smtplib.SMTPException as e:
                print('无法发送邮件')
        else:
            print('手机执行正常')

    def mobile_status(self):
        while True:
            try:
                cursor.execute(SELECT_HOUR)
                rows = cursor.fetchall()
                select_phones = list(map(lambda x: x[0].strip().replace('\ufeff', ''), rows))
                # 查询差集
                problem_phones = set(mobiles).difference(set(select_phones))
                # send email
                XiaoMiCheckTool.send_email(self, problem_phones)
            except Exception as e:
                print(e)
            finally:
                # 十分钟
                time.sleep(60 * 10)


if __name__ == '__main__':
    xm = XiaoMiCheckTool()
    xm.mobile_status()

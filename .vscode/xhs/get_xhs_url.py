import requests
import json
import pymssql
import time
import datetime

# 小红书url
url = 'https://www.xiaohongshu.com/explore'
# 社区精选
js_url = 'https://www.xiaohongshu.com/fe_api/burdock/v1/homefeed/notes?page_size=20&oid=recommend&page=1'
# url
base_url = 'https://www.xiaohongshu.com/discovery/item/'

sql_server = '192.168.2.72'

conn = pymssql.connect(sql_server, 'WebTest1',
                       'WebTest1', 'Jeqee_Navy_RedBook')

insert_sql = 'INSERT INTO [dbo].[RedBookGetData] VALUES (\'%s\', \'%s\', \'%s\', %d, \'%s\', %s, \'%s\', %d, \'%s\')'

select_sql = 'SELECT TOP 1 * FROM [RedBookGetData] WHERE TargetUid = \'%s\''

update_sql = 'UPDATE RedBookGetData SET Times = Times + 1 WHERE TargetUid = \'%s\''

cursor = conn.cursor()
if not cursor:
    raise Exception('数据库链接失败')
chrome_header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                 'Accept-Encoding': 'gzip, deflate, br',
                 'Accept-Language': 'zh-CN,zh;q=0.9',
                 'Cache-Control': 'max-age=0',
                 'Connection': 'keep-alive',
                 'Cookie': 'xhsTrackerId=042b565f-cedf-487d-c8a4-955c81856c36; Hm_lvt_9df7d19786b04345ae62033bd17f6278=1565571814,1565571842,1565571864,1565594667; Hm_lvt_d0ae755ac51e3c5ff9b1596b0c09c826=1565571814,1565571842,1565571865,1565594667; xhs_spses.5dde=*; xhs_spid.5dde=e1532231aa4ba29f.1562565755.257.1569390620.1569382073.8f3aa343-7f91-4637-b562-71188d65a918',
                 'Host': 'www.xiaohongshu.com',
                 'Upgrade-Insecure-Requests': '1',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}


js_header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
             'Accept-Encoding': 'gzip, deflate, br',
             'Accept-Language': 'zh-CN,zh;q=0.9',
             'Cookie': 'xhsTrackerId=042b565f-cedf-487d-c8a4-955c81856c36; Hm_lvt_9df7d19786b04345ae62033bd17f6278=1565571814,1565571842,1565571864,1565594667; Hm_lvt_d0ae755ac51e3c5ff9b1596b0c09c826=1565571814,1565571842,1565571865,1565594667; extra_exp_ids=; xhs_spses.5dde=*; xhs_spid.5dde=e1532231aa4ba29f.1562565755.258.1569397278.1569391691.f8d6bfd7-f486-4d3e-bd67-be7a8d2ab1db',
             'Host': 'www.xiaohongshu.com',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
             'Referer': 'https://www.xiaohongshu.com/explore',
             'X-Sign': 'X6c1882474eb3d460da315588395744b6'}


def get_url():
    while True:
        res = requests.get(url, headers=chrome_header)
        if res.status_code == 200:
            # 访问主页
            # content = res.content.decode('utf-8')
            # print(content)
            hide_res = requests.get(js_url, headers=js_header)
            if hide_res.status_code == 200:
                content = hide_res.content.decode('utf-8')
                json_dic = json.loads(content)
                for data in json_dic['data']:
                    cursor.execute(select_sql % data['id'])
                    rows = cursor.fetchall()
                    if rows:
                        print('%s 数据库已存在 %s' %
                              (data['id'], time.strftime('%Y-%m-%d %H:%M:%S')))
                        cursor.execute(update_sql % data['id'])
                        continue
                    print(data)
                    # 新增数据库
                    print(insert_sql % (
                        data['user']['id'], data['id'], data['link'], data['likes'], data['title'], 1 if(data['is_liked']) else 0, data['user']['nickname'], 1, time.strftime('%Y-%m-%d %H:%M:%S')))
                    cursor.execute(insert_sql % (data['user']['id'], data['id'], data['link'], data['likes'], data['title'], 1 if(
                        data['is_liked']) else 0, data['user']['nickname'], 1, time.strftime('%Y-%m-%d %H:%M:%S')))
                conn.commit()
            time.sleep(60*60)
        else:
            print('请求失败:%s' % hide_res.status_code)
            time.sleep(30 * 60)
        pass


if __name__ == "__main__":
    get_url()
    # handle_content()

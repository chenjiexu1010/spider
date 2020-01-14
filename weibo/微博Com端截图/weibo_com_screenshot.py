# -*- coding:utf-8 -*-
# !/usr/bin/Python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import json
from selenium import webdriver
import time

# 代理用户名密码
ProxyUsername = "jeqee"
ProxyPassword = "jeqeeproxy"


# 禁止弹窗
# prefs = {
#     'profile.default_content_setting_values': {
#         'notifications': 2
#     }
# }
# options.add_experimental_option('prefs', prefs)


def create_proxyauth_extension(proxy_host, proxy_port, proxy_username, proxy_password,
                               scheme='http', plugin_path=None):
    """Proxy Auth Extension

       args:
           proxy_host (str): domain or ip address, ie proxy.domain.com
           proxy_port (int): port
           proxy_username (str): auth username
           proxy_password (str): auth password
       kwargs:
           scheme (str): proxy scheme, default http
           plugin_path (str): absolute path of the extension

       return str -> plugin_path
       """
    import string
    import zipfile
    if plugin_path is None:
        plugin_path = '/tmp/vimm_chrome_proxyauth_plugin.zip'
    manifest_json = """
       {
           "version": "1.0.0",
           "manifest_version": 2,
           "name": "Chrome Proxy",
           "permissions": [
               "proxy",
               "tabs",
               "unlimitedStorage",
               "storage",
               "<all_urls>",
               "webRequest",
               "webRequestBlocking"
           ],
           "background": {
               "scripts": ["background.js"]
           },
           "minimum_chrome_version":"22.0.0"
       }
       """

    background_js = string.Template(
        """
        var config = {
                mode: "fixed_servers",
                rules: {
                  singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                  },
                  bypassList: ["foobar.com"]
                }
              };
 
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
 
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }
 
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )
    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path


# 禁用GPU
# options.add_argument('disable-gpu')

# 获取代理ip
def get_proxy_ip():
    ip = ''
    try:
        proxy_result = requests.get('http://192.168.2.74:25003/api/GetRandomProxy')
        if proxy_result.status_code == 200:
            info = json.loads(proxy_result.content.decode('utf-8'))
            ip = info['_ProxyAddress']
    except Exception as e:
        pass
    return ip


# 关键词mid匹配截图
def weibo_com_screenshot(key_world, mid):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=800,800')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-gpu')
    # options.add_argument('--headless')
    # proxy_info = get_proxy_ip()
    # if not proxy_info:
    #     print('代理获取失败')
    # ip = proxy_info.split('/')[2].split(':')[0]
    # port = proxy_info[-6:-1]
    # proxyauth_plugin_path = create_proxyauth_extension(
    #     proxy_host=ip,
    #     proxy_port=port,
    #     proxy_username=ProxyUsername,
    #     proxy_password=ProxyPassword
    # )
    # options.add_argument("--start-maximized")
    # options.add_extension(proxyauth_plugin_path)
    browser = webdriver.Chrome(options=options, executable_path='chromedriver.exe')
    browser.set_script_timeout(1)
    try:
        browser.get('https://s.weibo.com/weibo?q=%s&Refer=SWeibo_box' % key_world)
        # browser.get(
        #     'http://httpbin.org/ip')
        # 等待页面加载完成
        time.sleep(5)
        # 获取页面源代码
        # page_source = browser.page_source
        mid_elements = browser.find_elements_by_xpath('//div[@mid]')
        for i in range(0, mid_elements.__len__()):
            if i == 0:
                continue
            if mid in mid_elements[i].get_attribute('mid'):
                try:
                    browser.execute_async_script(
                        "document.getElementsByClassName('card-wrap')[%d].style.border = '2px solid red'" % i)
                except Exception as ex:
                    try:
                        browser.execute_async_script(
                            "window.scrollTo(0, %d)" % mid_elements[i].location['y'])
                    except Exception as ex2:
                        pass
                # TODO 修改浏览器高度无效  设置浏览器高度
                browser.set_window_size(width=800, height=800 + mid_elements[i].location['y'])
                try:
                    browser.execute_async_script(
                        "window.scrollTo(0, 0)")
                except Exception as ex3:
                    pass
                browser.save_screenshot('test.png')
                print('成功截到图mid:%s' % mid)
                break
    except Exception as e:
        print(e)
    finally:
        # 关闭浏览器
        browser.quit()


if __name__ == '__main__':
    weibo_com_screenshot('海外婚礼', '')

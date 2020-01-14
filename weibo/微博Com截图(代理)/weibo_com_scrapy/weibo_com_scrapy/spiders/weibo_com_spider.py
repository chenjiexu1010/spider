# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import scrapy


class WeiBoCom(scrapy.Spider):
    name = 'weibo_com'
    # allowed_domains = ['bing.com']
    start_urls = ['https://s.weibo.com/weibo?q=海外婚礼&Refer=SWeibo_box']

    # bash_url = 'https://www.baidu.com/'

    def spider_closed(self):
        self.driver.quit()

    def start_requests(self):
        full_url = 'https://s.weibo.com/weibo?q=海外婚礼&Refer=SWeibo_box'
        yield scrapy.Request(full_url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        print('--进入callback--')
        page = response.url.split("/")[-2]
        filename = 'E:\\quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        # self.driver.get('http://httpbin.org/ip')
        # self.driver.set_window_size(width=800, height=800)
        # self.driver.save_screenshot('test.png')
        # item = WbscrapyItem()

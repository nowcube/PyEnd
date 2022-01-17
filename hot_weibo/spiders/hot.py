# -*- coding:utf-8 -*-  
import scrapy
from scrapy.http.request import Request

class HotWeibo(scrapy.Spider):
    name="hot"
    start_urls = [
        'https://s.weibo.com/top/summary'
    ]

    def parse(self, response):
        for title in response.xpath('//div[@class="data"]//tbody//td[@class="td-02"]/a/text()').extract():
            # print(title)
            # print('https://s.weibo.com' + response.xpath('//div[@class="data"]//tbody//td[@class="td-02"]/a/@href').extract_first())
            if title:
                yield {
                    "title": title,
                    "url": 'https://s.weibo.com' + response.xpath('//div[@class="data"]//tbody//td[@class="td-02"]/a/@href').extract_first()
                }
        # title = response.xpath('//div[@class="data"]//tbody//td[@class="td-02"]/a/text()').extract()
        # print(title)
        # print(response.url)    
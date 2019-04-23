# -*- coding: utf-8 -*-
import scrapy


class XinlangspiderSpider(scrapy.Spider):
    name = "xinlangspider"
    allowed_domains = ["news.sina.com.cn/roll/#pageid=153"]
    start_urls = ['http://news.sina.com.cn/roll/#pageid=153/']

    def parse(self, response):
        # print(response.body )
        pass
        print(response.xpath('//head/title/text()').extract_first())
        print(response.xpath('//div[@style="overflow:hidden"]').extract())  #

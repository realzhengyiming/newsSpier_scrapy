# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

from scrapy import signals

from scrapy.conf import settings   # 这儿需要注意导入

from requests_html import HTMLSession




class ImagespiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s


    def process_request(self,request,spider):  # 后期可以改成使用requests-html的版本把，比较新。
        print("使用自定义请求")
        print(spider.name)
        ua = random.choice( settings["USER_AGENT_LIST"] )
        print(ua)
        request.headers['User-Agent'] = ua  # 提取到的ua随机设置给请求

        # referer = "https://gczfl01.com"  # 这个先闭
        # if referer:
        #     request.headers['referer'] = referer
        # 设置代理,需要使用的时候使用，并且记得settings中设置，或者维护的代理池中提取（数据库）
        # proxy = random.choice( settings["PROXY"] )
        # request.meta['proxy'] = proxy





        pass

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

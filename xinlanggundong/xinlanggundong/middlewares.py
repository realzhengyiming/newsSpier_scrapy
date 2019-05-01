# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import time
import scrapy
from scrapy import signals

from scrapy.conf import settings   # 这儿需要注意导入
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# # todo
# class SeleniumMiddlerware(object):
#     """
#     利用selenium，获取动态页面数据
#     """
#     def process_request(self, request, spider):
#         print("正在调用请求哈")
#         chrome_options = Options()
#         chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
#         chrome_options.add_argument('--disable-gpu')
#         chrome_options.add_argument('--no-sandbox')
#         # 指定谷歌浏览器路径  ,寻找一个对应版本的chrome驱动去才可以。 todo
#         self.driver = webdriver.Chrome(chrome_options=chrome_options,
#                                        executable_path=r'D:\chromedriver')
#         if request.url:  #不为什么的话，这个代码怎么搞呢。
#             self.driver.get(request.url)
#             time.sleep(1)  # 这儿设置了限速，手动限速
#             html = self.driver.page_source
#             self.driver.quit()
#             print("这儿是解析的requests")
#             # print(html)  这个暂时可以注释掉
#             return scrapy.http.HtmlResponse(url=request.url, body=html.encode('utf-8'), encoding='utf-8',
#                                             request=request)


class XinlanggundongSpiderMiddleware(object):

    # 1这个是静态的设置配置id，启用这个就可以了
    def process_request(self,request,spider):
        # 自动生成的这儿直接增加设置ua 的部分,手动增加部分
        print("现在使用—》自己定义好的UA")
        ua = random.choice( settings["USER_AGENT_LIST"] )
        print(ua)
        request.headers['User-Agent'] = ua  # 提取到的ua随机设置给请求

        # 设置代理,需要使用的时候使用，并且记得settings中设置，或者维护的代理池中提取（数据库）
        # proxy = random.choice( settings["PROXY"] )
        # request.meta['proxy'] = proxy
        pass

    # def process_request(self, request, spider):
    #     referer = request.url
    #     if referer:
    #         request.headers['referer'] = referer  chrome如何设置referer


    # 2这个是chrome 调用的。  重要的是找正确版本的chromedriver才可以用的样子。
    # def process_request(self, request, spider):
    #     print("正在调用chrome请求")
    #     print("现在使用—》chrome发起请求")

    #     chrome_options = Options()
    #     chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
    #     chrome_options.add_argument('--disable-gpu')
    #     chrome_options.add_argument('--no-sandbox')
    #     # 指定谷歌浏览器路径
    #     driver = webdriver.Chrome(chrome_options=chrome_options,
    #                                    executable_path=r'D:/chromedriver')
    #     if request.url :  #不为什么的话，这个代码怎么搞呢。
    #         driver.get(request.url)
    #         time.sleep(0.8)  # 这儿设置了限速，手动限速
    #         html = driver.page_source
    #         driver.quit()
    #         # print("这儿是解析的requests")
    #         # print(html)  这个暂时可以注释掉
    #         return scrapy.http.HtmlResponse(url=request.url, body=html.encode('utf-8'), encoding='utf-8',
    #                                         request=request)


    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# -*- coding: utf-8 -*-
# 这儿改成是腾讯的就可以了。
import traceback
import scrapy
from bs4 import BeautifulSoup
from scrapy.loader import ItemLoader
import time
from Crawler.spiders.spider_expends import TengxunExpend
from ..items import  News


class TengxunSpider(scrapy.Spider) : # 这边是没什么问题的了
    name = 'tengxun'
    allowed_domains = ["qq.com"]
    start_urls = [
        # 'http://roll.news.qq.com/'
        # 'https://news.qq.com/a/20190513/007759.htm', 测试用个案网页。
        # 'https://news.qq.com/a/20190512/004148.htm',
        # 'https://news.qq.com/a/20190514/000037.htm',
        # 'https://news.qq.com/a/20190513/005746.htm'
    ]

    count = 1

    def close(spider, reason):
        print("腾讯的爬虫爬完了。")
    # 这儿重写一下，我只写页面的具体内容的解析就可以了。
    def start_requests(self):
        tengxun_expend = TengxunExpend()
        self.start_urls = tengxun_expend.pageUrlMain()  # 测试暂时改了
        for url in self.start_urls:
            print()
            print(url)
            yield scrapy.Request(url, dont_filter=False)
        #     # 这里重写爬虫入口方法，将dont_filter设置为false
        #     # 是为了让起始url放入srcapy.Request请求url池中，对起始url也做去重处理
        #     # 一次是分页数据里检索到的第一页


    def parse(self, response):  # 每一页的都在这儿了。
        main = response.xpath("//*[@class='Cnt-Main-Article-QQ']")[0]
        print(main)  # xpath object
        title, Hcontent, Tcontent, Acontent = "", "", "", ""  # 最后一个参数好像没什么用
        try:
            title = response.xpath("//head/title/text()").extract_first()

            newdate = response.xpath("//span[@class='a_time']/text()").extract_first().split(" ")[0]
            lenP = main.xpath("p")
            print(len(lenP))
            if len(lenP) > 2:  # 为2的好像是纯视频的，还有一个文字描述的这种。
                Hcontent = lenP[0].extract()

                for p in main.xpath("p"):
                    simpleP = p.extract()
                    Acontent += simpleP

                # Tcontent = "".join(BeautifulSoup(Acontent, 'lxml').text)
                # print(title)
                # print()
                # print(Acontent)
                # print()
                # print(Tcontent)
                # print()
                # print(Hcontent)
                # print()
                newsloader = ItemLoader(item=News(), response=response)   # 但是使用这种方法插入进去的都会是list。
                newsloader.add_value('title', title)
                newsloader.add_value('Acontent', Acontent)
                # newsloader.add_value('Tcontent', Tcontent)  # 统一管道进行处理
                newsloader.add_value('Hcontent', Hcontent)
                newsloader.add_value('url', response.url)
                newsloader.add_value('urlState', "True")
                newsloader.add_value('fromWhere', "tengxun")
                newsloader.add_value("newdate",newdate)

                yield newsloader.load_item()
                print(newsloader.load_item())
                # time.sleep(180)

            else:
                print("这个为纯视频的新闻，无文本，正在跳过。")

        except Exception as e:
            print(e)
            traceback.print_exc()  # 貌似这个，一个错



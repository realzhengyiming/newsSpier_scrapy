# -*- coding: utf-8 -*-
# 这儿改成是腾讯的就可以了。
import traceback
from datetime import timedelta,date
import scrapy
import time
from bs4 import BeautifulSoup
from scrapy.loader import ItemLoader

from Crawler.items import News
from Crawler.settings import CRAWL_DELAY_DAY
from Crawler.spiders.spider_expends import WangyiExpend


class WangyiSpider(scrapy.Spider) : # 这边是没什么问题的了
    name = 'wangyi'
    allowed_domains = ["163.com"]  #
    start_urls = [
        # 'https://news.163.com/19/0514/04/EF4400KC0001899N.html',
        # 'https://news.163.com/19/0514/06/EF49KV8A00018AOR.html'

    ]

    count = 1

    def close(spider, reason):
        print("网易的爬虫爬完了。")
    # 这儿重写一下，我只写页面的具体内容的解析就可以了。

    def start_requests(self):
        wangyi_expend = WangyiExpend()
        self.start_urls = wangyi_expend.getRollUrlList()  # 默认都是获得昨天的新闻。
        for url in self.start_urls:
            # print()
            # print(url)
            yield scrapy.Request(url, dont_filter=False)



    def parse(self, response):  # 每一页的都在这儿了。
        throwSrcPart =  (date.today() + timedelta(days=-CRAWL_DELAY_DAY)).strftime("%Y/%m/%d")  # settings里面有
        print(throwSrcPart)

        title, Hcontent, Tcontent, Acontent = "", "", "", ""  # 最后一个参数好像没什么用
        try:
            title = response.xpath("//head/title/text()").extract_first()
            mainP = response.xpath("//div[@class='post_text']")[0]
            # print(mainP.extract())
            for p in mainP.xpath("p"):
                pp = p.xpath("img/@src").extract()
                # print(p)
                if len(pp) !=0 : # 找到有图片
                    # print("找到图片")
                    # print(pp[0])
                    if pp[0].find(throwSrcPart)!=-1:
                        print(pp[0])
                        print("丢弃这个p")
                    else:
                        Acontent += p.extract()

                else:
                    Acontent += p.extract()

            # time.sleep(60)
            # print(Acontent)
            lastDayDate =  (date.today() + timedelta(days=-CRAWL_DELAY_DAY)).strftime("%Y-%m-%d")  # settings里面有
            tempAcontent = BeautifulSoup(Acontent, 'lxml')
            # Tcontent = "".join(tempAcontent.text)

            lenP = tempAcontent.find_all("p")
            print(len(lenP))
            if len(lenP) > 2:  # 为2的好像是纯视频的，还有一个文字描述的这种。
                Hcontent = str(lenP[0])
                print("Hcontent")
                print(Hcontent.replace(r'\n',""))


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
            # newsloader.add_value('Tcontent', Tcontent)  # 这个字段统一给管道进行处理
            newsloader.add_value('Hcontent', Hcontent)
            newsloader.add_value('url', response.url)
            newsloader.add_value('urlState', "True")
            newsloader.add_value('fromWhere', "wangyi")
            newsloader.add_value("newdate",lastDayDate)

            yield newsloader.load_item()
            print(newsloader.load_item())
                # time.sleep(180)

            # else:
            #     print("这个为纯视频的新闻，无文本，正在跳过。")

        except Exception as e:
            print(e)
            traceback.print_exc()  # 貌似这个，一个错



# -*- coding: utf-8 -*-
import json
from datetime import date, timedelta

import pysnooper  # debug 用的包
import scrapy
from scrapy.loader import ItemLoader
import time

from ..items import News
from ..items import NewsContent



class XinlangspiderSpider(scrapy.Spider):
    name = 'news'
    # 爬取的域名，不会超出这个顶级域名
    allowed_domains = ['sina.com']  # 可以设置成不过滤吗。
    start_urls = [
    ]

    count = 1
    # {}占位符，用于字符串替换，将获取到的/text/page/1格式内容替换成完整url  这个是新浪新闻的。滚动新闻的页面
    host_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page={}'

    def start_requests(self):
        for num in range(1,60):  # 这儿是看爬取多少页的。50*60 =3000 已经够多的了。新浪的
            print(self.host_url.format(num))
            self.start_urls.append(self.host_url.format(num))
        for url in self.start_urls:  # 第一层算是广度优先爬取对吧。
            yield scrapy.Request(url, dont_filter=False)
        #     # 这里重写爬虫入口方法，将dont_filter设置为false
        #     # 是为了让起始url放入srcapy.Request请求url池中，对起始url也做去重处理
        #     # 否则会爬取到两次 https://www.qiushibaike.com/text/，一次是起始url
        #     # 一次是分页数据里检索到的第一页


    def parse(self, response):  # 每一页的都在这儿了。
        # itemloader
        allDic = json.loads(response.body)
        # print(allDic)
        print(type(allDic))
        for one in allDic['result']['data']:
            # print(one['url'])
            # print(one['title'])
            timeStamp = one['intime']
            timeArray = time.localtime(int(timeStamp))
            newsDatetemp = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            newsDate = newsDatetemp.split(" ")[0]   # 这个是日期的字符串
            # print(newsDate)
            # print(one['intime'])

            # 这儿做一个测试，用来看是不是在同一个地方的。不要当天的，这儿注意
            lastDay = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")  # 获取昨天日期
            lastDayEnd = (date.today() + timedelta(days=-2)).strftime("%Y-%m-%d")  # 获取前天日期

            # 第二天爬取会出现今天的，还有昨天的，还有前天的。
            if newsDate == lastDay:
                # 添加进item
                itemloader = ItemLoader(item=News(), response=response, )
                itemloader.add_value('url', one['url'])
                itemloader.add_value('title', one['title'])
                itemloader.add_value('timestamp', one['intime'])
                itemloader.add_value('newsDate', newsDate)
                resultItem = itemloader.load_item()
                yield scrapy.Request(url=resultItem['url'][0], callback=self.newsContent, dont_filter=True,
                                     meta={"lastItem": resultItem})

            if newsDate == lastDayEnd: # 这个是前天的
                break  # 这儿就是跳出循环了

            else:    # 是今天的情况就不用管了
                print("这条是今天的，跳过爬取---》因为我们要提取完整的昨天的新闻。😁")
                print()
        # print("这儿这个就是跑完了！")

    # 这边是解析详情页的部分。
    @pysnooper.snoop()  #这样就可以debug了
    def newsContent(self,response):
        print()
        print()
        lastItem = response.meta["lastItem"]
        print(lastItem['url'][0])
        print(lastItem['title'][0])
        print(lastItem['newsDate'][0])
        # print(response.body)
        contentlist = []
        print("全文在这儿了")
        # print(response.xpath("//div[@class='article']").xpath('string(.)').extract_first())
        for allp in response.xpath("//div[@class='article']"):   # //div[@class='article'] ，要取这下面的所有的文本对吧
            print(allp.xpath("p"))
            for p in allp.xpath("p"):
                # print(p.xpath("text()").extract_first())
                contentlist.append(p.xpath("string(.)").extract_first().strip())  # 换用这种后呢，会不会就不会再发生那种事情了。
            print()
        print()
        print(contentlist)
        # time.sleep(60)

        # print(contentlist)    # todo 有时候是None的回去 研究一下这部分的部分
        print(len(contentlist))
        tempContent = ""
        if len(contentlist)== 0 :
            tempContent=""
        else:
            # 这儿可能回合并出错的。合并出错就再试一试咯。应该没什么大问题的。
            tempContent = "".join(contentlist)     # todo是这儿的问题把，也就是说可能contentlist里面并不是纯文本的。


        print("检查第几个{}".format(self.count))
        self.count=self.count+1
        print(tempContent)
        newsloader = ItemLoader(item=NewsContent(), response=response)
        newsloader.add_value('Pcontent',tempContent)
        newsloader.add_value('title',lastItem['title'][0])
        newsloader.add_value('url',lastItem['url'][0])
        newsloader.add_value("newsDate",lastItem['newsDate'][0])

        print(lastItem['newsDate'][0])
        # time.sleep(15)

        yield newsloader.load_item()
        # time.sleep(30)
        pass

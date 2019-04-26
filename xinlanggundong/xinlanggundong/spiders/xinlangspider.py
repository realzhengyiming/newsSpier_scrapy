# -*- coding: utf-8 -*-
import time

import scrapy

from xinlanggundong.items import XinlanggundongItem


class XinlangspiderSpider(scrapy.Spider):

    name = "xinlangspider"
    allowed_domains = ["news.sina.com.cn"]
    start_urls = ['https://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page=1']
    count = 0


    def start_requests(self):
        # 由此方法通过下面链接爬取页面 重写
        # 定义爬取的链接
        urls = [
            'https://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page=1'
            # 'http://lab.scrapyd.cn/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)  # 爬取到的页面如何处理？提交给parse方法处理

    # todo 刚开始有4个item怎么回事，好像是不一样的。分割开来了。
    # 这儿是生成后面的页面的url的
    def makeUrlList(self):
        # 通过url来进行合成
        tempList = []
        rawUrl = "https://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page="
        for num in range( 1 ,20 ):  # 50*50 =2500

            url = rawUrl+str(num)
            # print(url)
            tempList.append(url)
        print("生成url列表成功")
        return tempList

    # 这儿负责不断的翻页，生成每一页的url
    def parse(self, response):
        print(response.url )
        nextUrl = self.makeUrlList()
        # 生成下一页的url todo 如何准确的知道解析了后返回就可以了。遇到前一天的就停止也是可以的
        com =1
        for url in nextUrl:
            print("第一页%d"%com)
            print(url)
            com += 1
            yield scrapy.Request(url=url, callback=self.parsePageUrls , dont_filter=True)  # 为什么只执行了一次 False的话那就是

            # 这种默认貌似是不可以
            # yield response.follow(url,callback=self.parsePageUrls)



    # 这边是具体解析每一页的内容
    def parsePageUrls(self,response):
        self.count = self.count+1
        print("提取url中{}".format(self.count))

        print(response.xpath('//head/title/text()').extract_first())
        mainbody = response.xpath('//div[@id="d_list"]')  # xpath对象
        urlcount = 0
        for li in mainbody[0].xpath("//li"):
            newsItem = XinlanggundongItem()

            spanLIst = li.xpath("span")
            tempA = spanLIst[1].xpath("a")
            # print(tempA.xpath("@href").extract_first())
            # print(tempA.xpath("text()").extract_first())

            newsItem['newsUrl'] = tempA.xpath("@href").extract_first()
            newsItem['title'] = tempA.xpath("text()").extract_first()


            dateTimeStr = spanLIst[2].xpath("text()").extract_first()
            if dateTimeStr.find("-") != -1:

                templist = dateTimeStr.split(" ")[0].split("-")
                # print(templist)
                if len(templist) == 3:  # 包含年份的，说明不是今年的了
                    dateTime = "-".join(templist)
                    # print(dateTime)
                    newsItem['dateTime'] = dateTime
                else:  # 这种应该是当成当年处理的。
                    # 获得当前的年份
                    nowYear = time.strftime('%Y', time.localtime(time.time()))
                    # print(nowYear)
                    dateTime = nowYear + "-" + "-".join(templist)
                    # print(dateTime)
                    newsItem['dateTime'] =dateTime

            urlcount += 1

            # print(dateTimeStr)
            print(newsItem)
            yield newsItem
        print(urlcount)




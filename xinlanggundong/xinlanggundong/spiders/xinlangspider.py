# -*- coding: utf-8 -*-
import time

import scrapy


class XinlangspiderSpider(scrapy.Spider):

    name = "xinlangspider"
    allowed_domains = ["news.sina.com.cn"]
    start_urls = ['https://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page=1']


   # 这儿是生成后面的页面的url的
    def makeUrlList(self):
        # 通过url来进行合成
        tempList = []
        rawUrl = "https://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page="
        for num in range(2,50):  # 50*50 =2500

            url = rawUrl+str(num)
            print(url)
            tempList.append(url)
        print("生成url列表成功")
        return tempList


    def parse(self, response):  # 这儿负责不断的翻页，生成每一页的url
        print(response.url )
        nextUrl = self.makeUrlList()
        # 生成下一页的url todo 如何准确的知道解析了后返回就可以了。遇到前一天的就停止也是可以的
        com =1
        for url in nextUrl:
            print("第一页%d"%com)
            print(url)
            yield scrapy.Request(url=url, callback=self.parsePageUrls,dont_filter=True)  # 为什么只执行了一次
            # yield response.follow(url,callback=self.parsePageUrls)

            com+=1



    def parsePageUrls(self,response): # 这边是具体解析每一页的内容
        print(response.xpath('//head/title/text()').extract_first())
        mainbody = response.xpath('//div[@id="d_list"]')  # xpath对象
        urlcount = 0
        for li in mainbody[0].xpath("//li"):
            # print(li.extract())
            # for span in li.xpath("span"): # 一共有三个span这样子
            #     print(span.extract())
            spanLIst = li.xpath("span")
            tempA = spanLIst[1].xpath("a")
            print(tempA.xpath("@href").extract_first())
            print(tempA.xpath("text()").extract_first())

            dateTimeStr = spanLIst[2].xpath("text()").extract_first()
            if dateTimeStr.find("-") != -1:
                templist = dateTimeStr.split(" ")[0].split("-")
                print(templist)
                if len(templist) == 3:  # 包含年份的，说明不是今年的了
                    dateTime = "-".join(templist)
                    print(dateTime)
                else:  # 这种应该是当成当年处理的。
                    # 获得当前的年份
                    nowYear = time.strftime('%Y', time.localtime(time.time()))
                    print(nowYear)
                    dateTime = nowYear + "-" + "-".join(templist)
                    print(dateTime)
            urlcount+=1

            # print(dateTimeStr)
            print()
        print(urlcount)


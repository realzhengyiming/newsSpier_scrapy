# -*- coding: utf-8 -*-
import time

import scrapy


class XinlangspiderSpider(scrapy.Spider):
    name = "xinlangspider"
    allowed_domains = ["news.sina.com.cn/roll/"]
    start_urls = ['https://news.sina.com.cn/roll/']

    def parse(self, response):  # 这儿负责不断的翻页
        # print(response.body )

        pass

    def parseNextDetail(self,response): # 这边是具体解析每一页的内容
        print(response.xpath('//head/title/text()').extract_first())
        mainbody = response.xpath('//div[@id="d_list"]')  # xpath对象
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

            # print(dateTimeStr)
            print()


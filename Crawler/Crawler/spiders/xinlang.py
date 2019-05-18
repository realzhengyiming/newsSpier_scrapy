# -*- coding: utf-8 -*-
# todo 会卡住，这个问题怎么解决
import json
from datetime import timedelta,date
import pysnooper  # debug 用的包
import scrapy
from bs4 import BeautifulSoup
from scrapy.loader import ItemLoader
import time
from Crawler.settings import CRAWL_DELAY_DAY
from ..items import  News


class XinlangSpider(scrapy.Spider) :
    name = 'xinlang'
    # 爬取的域名，不会超出这个顶级域名
    allowed_domains = ['sina.com']  # 可以设置成不过滤吗。
    start_urls = [
    ]

    count = 1
    # {}占位符，用于字符串替换，将获取到的/text/page/1格式内容替换成完整url  这个是新浪新闻的。滚动新闻的页面
    host_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page={}'

    def close(spider, reason):
        print("网易的爬虫爬完了。")  #发邮件之类的。



    def start_requests(self):
        for num in range(1,100):  # 这儿是看爬取多少页的。一般56*100=5600
            print(self.host_url.format(num))
            self.start_urls.append(self.host_url.format(num))
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=False)
        #     # 这里重写爬虫入口方法，将dont_filter设置为false
        #     # 是为了让起始url放入srcapy.Request请求url池中，对起始url也做去重处理
        #     # 否则会爬取到两次 https://www.qiushibaike.com/text/，一次是起始url
        #     # 一次是分页数据里检索到的第一页
    def parse(self, response):
        # itemloader
        '''
            这儿只取昨天的。 这儿是把json中每一页的url提取出来，有两层的深度。
            url = scrapy.Field()
            urlState = scrapy.Field()
            title = scrapy.Field()
            Hcontent =  scrapy.Field()
            Tcontent = scrapy.Field()
            Acontent = scrapy.Field()
            newdate = scrapy.Field()
            fromWhere = scrapy.Field()
        :param response:
        :return:
        '''
        allDic = json.loads(response.body)
        # print(allDic)
        print(type(allDic))
        for one in allDic['result']['data']:
            itemloader = ItemLoader(item=News(), response=response )
            timeStamp = one['intime']
            timeArray = time.localtime(int(timeStamp))
            newsDatetemp = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            newsDate = newsDatetemp.split(" ")[0]
            print(newsDate)

            url = ""
            if "url" in one:
                # print("有url的")
                url = one["url"]
                pass # 有就直接提取这个
            elif "urls" in one:
                print("没有url")
                tempUrl  = one["urls"][0]
                url = tempUrl.replace("\/","/")

            print()
            # 添加进item
            lastDayDate =  (date.today() + timedelta(days=-CRAWL_DELAY_DAY)).strftime("%Y-%m-%d")  # settings里面有
            if newsDate ==lastDayDate: # 只取出昨天的新闻。特指只选择昨天的新闻，这样才对把
                itemloader.add_value('url',url)  # 这儿我发现了，有些是没有这个字段的
                itemloader.add_value('title', one['title'])
                itemloader.add_value('newdate', newsDate)
                resultItem = itemloader.load_item()  # item 也是可以传过去的，传过去继续填充。
                yield scrapy.Request(url=resultItem['url'][0],callback=self.newsContent,dont_filter=True,meta={"lastItem":resultItem})
            else:
                print("不是昨天的新闻，正在选择性跳过")


    # 这边是解析详情页的部分。
    @pysnooper.snoop()  #这样就可以debug了
    def newsContent(self,response):
        title, Hcontent, Tcontent, Acontent = "", "", "", ""  # 最后一个参数好像没什么用
        lastItem = response.meta.get("lastItem",None)  # 这样就可以避免不行的。

        # 这边这个开始是划分句子，用html代码就可以,为了提取首段
        contentlist = []
        for allp in response.xpath("//div[@class='article']"):   # //div[@class='article'] ，要取这下面的所有的文本对吧
            for p in allp.xpath("p"):
                print(p.extract())
                contentlist.append(p.extract())
                # contentlist.append(p.xpath("string(.)").extract_first().strip())  # 换用这种后呢，会不会就不会再发生那种事情了。
        print()
        print("全文中句子的数量有那么多{}".format(len(contentlist)))
        print(contentlist)
        if len(contentlist) > 0: #  是否是没有纯文本的新闻的处理写在管道里面就好了。
            print(contentlist[0]) # 取第一个作为首段的东西
            Hcontent = contentlist[0]

        # print("新闻的正文内容在这里。")
        Acontent = response.xpath("//div[@class='article']").extract_first()  # 这个就是str
        # Tcontent = "".join(BeautifulSoup(Acontent, 'lxml').text)
        if Tcontent=="":
            print(Tcontent)
            print(Acontent)
            print("可能为图片新闻")
            print(response.url)
            # time.sleep(10)

        newsloader = ItemLoader(item=News(), response=response)  # 但是使用这种方法插入进去的都会是list。
        newsloader.add_value('title', lastItem['title'][0])
        newsloader.add_value('Acontent', Acontent)
        # newsloader.add_value('Tcontent', Tcontent)  # 统一有管道进行处理
        newsloader.add_value('Hcontent', Hcontent)
        newsloader.add_value('url', response.url)
        newsloader.add_value('urlState', "True")
        newsloader.add_value('fromWhere', "xinlang")
        newsloader.add_value("newdate", lastItem['newdate'][0])


        yield newsloader.load_item()   # 这个扔给管道就可以了。
        print(newsloader.load_item())
        # time.sleep(60)




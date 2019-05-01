# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XinlanggundongItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    newsUrl = scrapy.Field() # 新闻链接
    title = scrapy.Field() # 新闻标题
    dateTime = scrapy.Field() # 新闻日期
    pass



# ---- 下面这儿是新增加的新闻爬取的，目前是新浪新闻
class News(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    timestamp = scrapy.Field()
    newsDate = scrapy.Field()


class NewsContent(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    Pcontent = scrapy.Field()
    newsDate = scrapy.Field()

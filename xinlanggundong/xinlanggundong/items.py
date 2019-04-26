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

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class ImagespiderItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     imgurl = scrapy.Field()
#     image_path = scrapy.Field()
#     pass
#
#
# class TextItem(scrapy.Item):
#     textTitle = scrapy.Field()  # title
#     #content = scrapy.Field()  # 这个是文章的正文。
#
#
# class simpleP(scrapy.Item):
#     simpleP = scrapy.Field()   # 这个是单独的句子  KEYI

# ------------这儿开始时新闻的。------------------ ,新浪的。
class Image(scrapy.Item):
    src = scrapy.Field()
    path = scrapy.Field()
    title = scrapy.Field()  # 或者说文件夹的名字。
    imagePath = scrapy.Field()



class NewsContent(scrapy.Item):  # 这个是具体的，图片也可以增回家一个字段把。
    url = scrapy.Field()
    title = scrapy.Field()
    Pcontent = scrapy.Field()
    timestamp = scrapy.Field()
    newsDate = scrapy.Field()
    imageUrls = scrapy.Field()  # 可以调用原来的生成
    imagePath = scrapy.Field()  # 保存在来相对位置

# ----------- 三大新闻的 item 写入tengxun 数据表的这个，暂时主要是这四个字段
class News(scrapy.Item):
    '''
    title = 标题
    Hcontent =   这个是首句的意思，暂时没怎么用到的样子。 有这几个就可以了,html代码的首段，是可能为只有一个图片的。
    Tcontent = 纯文字的全文吗
    Acontent = 这个是html 的全文。
    '''

    url = scrapy.Field()
    urlState = scrapy.Field()
    title = scrapy.Field()
    Hcontent =  scrapy.Field()
    Tcontent = scrapy.Field()
    Acontent = scrapy.Field()
    newdate = scrapy.Field()
    fromWhere = scrapy.Field()







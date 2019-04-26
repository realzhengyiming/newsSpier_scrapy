# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# return 回去的意思就是给剩下的管道使用。

class XinlanggundongPipeline(object):
    def process_item(self, item, spider):
        return item

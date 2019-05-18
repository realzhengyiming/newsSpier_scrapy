from scrapy import cmdline
# 同时启动所有的爬虫进行爬取工作。

if __name__ == '__main__':
    cmdline.execute("scrapy crawlall".split())

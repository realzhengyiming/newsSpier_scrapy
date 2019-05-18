from scrapy.commands import ScrapyCommand

from Crawler.expand_package.Comment import CommentCrawl
from Crawler.expand_package.DBcontrol import DB


class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def run(self, args, opts):
        spider_list = self.crawler_process.spiders.list()
        for name in spider_list:
            self.crawler_process.crawl(name, **opts.__dict__)
        self.crawler_process.start()
        print("三大站点的新闻正文爬取完毕了!")
        # todo 先是tengxun表——》django表的分类
        ## todo 分类还需要调用评分进行插入到里面。
        print("正在进行它新闻分类和情感得分分数录入...")
        dbtool = DB()
        dbtool.classifyDB()

        print("正在进行腾讯新闻评论的爬取...")
        commentC = CommentCrawl()
        commentC.getCommentMain()  # 测试主题从url中提取，url又可以合成。
        print("今天爬虫任务完成！")

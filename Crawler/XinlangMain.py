from scrapy import cmdline


if __name__ == '__main__':
    cmdline.execute("scrapy crawl xinlang".split())

    # print("哈哈哈")

    # todo 新浪的，不知道为什么会提取出当天的，我只要昨天的，这样比较整齐。
    # todo 明天把分类到那六个表还有把评论提取到剩下的那六个表的操作做完，然后再合并起来。
    # todo 统一在管道进行过滤处理把，爬虫内是可以不处理的。然后管道内的那儿用bs4去掉style的这种/script这种也是。
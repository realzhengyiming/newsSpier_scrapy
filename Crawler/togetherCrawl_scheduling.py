# -*- coding: utf-8 -*

import datetime
import multiprocessing
import os
import schedule
import time
from scrapy import cmdline
# 同时启动所有的爬虫进行爬取工作。
from Crawler.settings import CRAWLALL_RUN_TIME


def worker_1(interval):
    print ("开始所有爬虫工作")
    cmdline.execute("scrapy crawlall".split())




class AutoRunAtTime:              #这儿只是一个线程的
    def job(self,name):   #这个是主线程把
        print("正在爬取今天的新闻内容")
        print('这里是进程: %sd   父进程ID：%s' % (os.getpid(), os.getppid()))
        p1 = multiprocessing.Process(target=worker_1, args=(6,))
        # p3 = multiprocessing.Process(target=worker_3, args=(4,))

        p1.daemon = True
        # p2.daemon = True

        p1.start()
        # p2.start()
        # p3.start()
        print("The number of CPU is:" + str(multiprocessing.cpu_count()))
        for p in multiprocessing.active_children():
            print("child   p.name:" + p.name + "\tp.id" + str(p.pid))

        p1.join()
        # p2.join()


    def startAutoRun(self,timeSet):         #24小时制的时间输入，传入一个时间的字符串
        name = "scrapy_news"
        schedule.every().day.at(timeSet).do(self.job, name)  # 应该也是24小时制的，记得  “输入24小时制的时间字符串
        while True:
            schedule.run_pending()
            # print("等待下一次...")
            time.sleep(1)


if __name__=="__main__":
    autoRun = AutoRunAtTime()
    print(time.strftime('%Y.%m.%d', time.localtime(time.time())))
    print("现在的时间是")
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    autoRun.startAutoRun(CRAWLALL_RUN_TIME)    #测试直接这儿写运行时间比较方便









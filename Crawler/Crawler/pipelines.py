# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
from datetime import date, timedelta

from bs4 import BeautifulSoup

from Crawler.expand_package.WordCloud import Gen_WordCloud
from Crawler.items import  News  # 这样导入才可以认识的啊
from Crawler.items import Image,NewsContent   # 这样导入才可以认识的啊
from Crawler.expand_package.picDownloadScript import Download
from Crawler.settings import CRAWL_DELAY_DAY, DOWMLOAD_IMG_IN_ACONTENT, MAKE_WORDCLOUD_STORE

from Crawler.expand_package.DBcontrol import DB


class newsPipeline(object):   # 自己写的这个处理图片的管道,统一一个管道处理就可以了吗。
    def __init__(self):
        # 一个管道的下载的部分是一样的。
        self.downloadTool = Download(None)  # setting 中设置默认的地址。
        # todo 增加mysql数据库组件也是一样的。
        self.crawlDelayDay = CRAWL_DELAY_DAY # 默认是爬取昨天的
        self.db = DB()

    def makeDateFolder(self): #
        crawl_date = (date.today() + timedelta(days=-self.crawlDelayDay)).strftime("%Y%m%d")  # 昨天日期
        return crawl_date

    # def setFileTitle(self, title):
    #     fileName = re.sub('[\/:*?"<>|]', '-', title)  # 去掉非法字符
    #     return fileName




    def downloadAndChangeImgPath(self,html_have_img,newsDate) -> str :
        '''
        :param html_have_img:  新闻的正文的html
        :param newsDate:   新闻的日期（用来做下载图片的文件名）
        :return:  img 中的src修改成下载到本地的地址
        '''
        print("正在下载正文中")
        soup = BeautifulSoup( html_have_img , 'lxml')
        for img in soup.find_all("img"):
            tempSrc = img['src']
            if tempSrc.find("http:") == -1:  # 默认可能漏掉了这部分的
                tempSrc = "http:" + tempSrc
                # time.sleep(1)
            fixedSrc = self.downloadTool.downloadImg(
                img_url=tempSrc,
                imgName=None,
                referer=None, now_date=newsDate)  # 这个是下面新建力的文件夹,默认都是延迟一天的。
            img['src'] = fixedSrc  # 这个地址放回去
            # 下载，返回path，然后修改。
            print(img['src'])
        print("图片下载并且修改src完成。")
        return [str(soup.extract()).replace("'", '"')]


    def fillter_Acontent(self,Acontent):  # clean_the_Acontent which hava  style or script
        soup = BeautifulSoup(Acontent, 'lxml')
        [s.extract() for s in soup("style")]
        [s.extract() for s in soup("script")]
        return str(soup)

    def process_item(self, item, spider):
        if isinstance(item, NewsContent):
            print("管道进来了！")
            if "imageUrls" in item: # 有图片才下载图片  这边的item还可以修改吗
                if len(item['imageUrls']) != 0:
                    print(item['imageUrls'])
                    downPath = []
                    for url in item['imageUrls']:
                        tempPath = self.downloadTool.downloadImg(
                            img_url=url,
                            imgName=None,
                            referer=None, now_date=self.makeDateFolder())  # 这个是下面新建力的文件夹
                        downPath.append(tempPath)  # 这个也是一个list 下载地址的。

                    downPathList=""
                    # todo 这个是用来放回去的 。
                    for path in downPath: # 当成独立的<p>
                        downPathList = downPathList+"<p><img src={0} /></p>".format(path)
                        print(downPathList)
                        # item['imagePath']
            else:
                print("这个item没有图片")
                print(item['url'])
            # 返回item
            self.db.insert(item['url'])
            return item

        elif isinstance(item,Image):
            if "src" in item: # 有图片才下载图片  这边的item还可以修改吗
                if len(item['src']) != 0:
                    print(item['src'])
                    downPath = []
                    print(item['title'])
                    for url in item['src']:
                        tempPath = self.downloadTool.downloadImg(
                            img_url=url,
                            imgName=None,
                            referer=None, now_date=(item['title'][0])) # 这个是下面新建力的文件夹
                        downPath.append(tempPath)
                    item['imagePath'] = downPath
            return item
            pass

        elif isinstance(item, News):  # 这儿是 新闻爬虫的。
            print("正在处理item")
            # 下载图片还有修改Acontent中的img

            if item['Acontent'][0].find("img") != -1 and DOWMLOAD_IMG_IN_ACONTENT:  # 发现纯文本的这里面有图片。才执行这个下载图片
                print("新闻中有图片，正在本地化处理......")
                print(item['url'])
                # 这儿注释掉，暂时不用，节省空间。下载图片不下载
                item['Acontent'] = self.downloadAndChangeImgPath(item['Acontent'][0],item['newdate'][0])  # 插入数据库，需要把’变成”,下载失败的就没有本地化
            print("正在插入数据库")
            if item['Acontent'][0]!="":  # 这儿是填充Tcontent 纯文本字段
                # 用bs4
                item['Acontent']= [self.fillter_Acontent(item['Acontent'][0])]  # 先过滤一下Acontent中奇怪的标签。
                item['Tcontent'] =[ "".join(BeautifulSoup(item['Acontent'][0], 'lxml').text)]
                self.db.insertItem(item)
                print("插入成功数据库")
            if item['Tcontent'][0]!="" and MAKE_WORDCLOUD_STORE: # 不是空文本的情况下是可以生成词云图的。
                # 把url生成唯一的md5作为词云的文件名
                # 前台调用只需要用这个方法生成一下md5就行了，也是唯一的值。       前端需要注意这儿！
                Gen_WordCloud(Newsid=self.downloadTool.makeMd5(item['url'][0]) , text=item['Tcontent'][0])
            # time.sleep(60)
            else: # 没有词云，那就只能用默认的了。
                pass
                print("为无文本新闻")
                print(item['url'][0])
            return item
            pass


        else:
            print("判断这个不是管道。")
            print(item)
            return item




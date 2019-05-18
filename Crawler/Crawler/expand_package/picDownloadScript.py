# -*- coding: utf-8 -*

# 下载到的一个路径中去，把图片下载下来，并且把新闻里面的
import hashlib
import os
import time
import traceback
import requests  ##导入requests

# from config import downloadPath
from Crawler.settings import IMAGES_STORE  # 这个是自己定义好的配置文件，一般可以放在相同目录下，可以直接访问。

class Download:
    def __init__(self, path):  # 先设置好下载的路径
        if (path == None):
            self.path = IMAGES_STORE  # 这边也直接使用默认使用配置文件的地址
            print("是 None")  # 每次管道也是还是重新生成的一个啊
        else:
            self.path = path

    def makeMd5(self,url):
        obj = hashlib.md5()
        obj.update(bytes(url,encoding="utf-8"))
        return obj.hexdigest()

    def downloadImg(self, img_url, imgName, referer, now_date):  # 这个下载的模块是没有返回值的,
        time.sleep(0.5)
        '''
        img_url,  图片的下载链接
        imgName,  下载的图片的名字
        referer,  这个参数是请求的时候防止加了referer参数的反反爬虫用的。
        now_date  图片下载到 指定路径下的什么文件夹内，这儿是使用 日期字段  作为文件夹 测试可以随意修改
        设置根据图片的url生成唯一的md5码，scrapy 类似的。
        '''
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            'Referer': referer}  ##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
        try:
            # int(shit)    # todo 图片可以不下载了
            img = requests.get(img_url, headers=headers)
            # print(img)
            # print(self.path)
            if (False == os.path.exists(os.path.join(self.path, now_date))):  # 不存在这个目录的话
                os.makedirs(self.path + '/' + now_date)
            if imgName==None:  # 不设置的话，默认就是md5
                imgName = self.makeMd5(img_url)  #改良过后通过url来生成唯一的md5的
            dPath = os.path.join(self.path, now_date, imgName + '.jpg')  # imgName传进来不需要带时间
            # print(dPath)
            print("图片的文件名 " + dPath)
            f = open(dPath, 'ab')
            f.write(img.content)
            f.close()
            # print("下载成功")
            return os.path.join( now_date, imgName + '.jpg')  # 返回相对路径
        except Exception as e:
            print(img_url)
            print(e)
            traceback.print_exc()


if __name__ == "__main__":
    # 局部测试代码
    imgUrl = "http://inews.gtimg.com/newsapp_match/0/5403685404/0"
    downloadTool = Download(None)  # todo 这儿有一个问题就是，这个图片的下载地址网页部分是带地址的，所以，最好的是网页部分不需要要再加上地址的文件夹，统一使用
    path = downloadTool.downloadImg(img_url="http://img1.gtimg.com/datalib_img//18-07-03/a/fda81a84eb06919ba40782c45ebbc28d.jpg" ,
                             imgName = None,
                             referer = None,
                             now_date = "20190505") # 这个是下面新建力的文件夹
    print(path)
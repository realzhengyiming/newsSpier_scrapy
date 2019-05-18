import random
from pprint import pprint

import chardet
import requests
from datetime import date, timedelta
from Crawler.settings import CRAWL_DELAY_DAY


class TengxunExpend:

    def returnThemeCode(self, theme):  # 这个是有用的，用来组合主题代码url的
        ent_Theme = 1537876288634
        sport_Theme = 1537877689177
        finance_Theme = 1537878365483
        tech_Theme = 1537879684280
        auto_Theme = 1537887032223
        house_Theme = 1537887128904
        news_Theme = 1537874915062
        if theme == 'news':
            return news_Theme
        if theme == 'ent':
            return ent_Theme
        if theme == 'sports':
            return sport_Theme
        if theme == 'tech':
            return tech_Theme
        if theme == 'auto':
            return auto_Theme
        if theme == 'house':
            return house_Theme
        if theme == 'finance':
            return finance_Theme

    def getThemeUrl(self, theme, today, pageNumber):
        rawUrl = "http://roll.news.qq.com/interface/cpcroll.php"
        rawReferer = '.qq.com/articleList/rolls/'  # 'http://news   前面还有这个东西
        print(theme)
        print(today)
        print(pageNumber)

        my_headers = [
            'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30',
            'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
            'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)']
        headers = {"User-Agent": random.choice(my_headers), 'Referer': 'http://' + theme + rawReferer}  # 默认值
        rawUrl = rawUrl + "?callback=rollback&mode=1&cata=&_=" + str(
            self.returnThemeCode(theme)) + "&site=" + theme + "&page=" + str(pageNumber) + "&date=" + today
        print(rawUrl)
        try:
            rawhtml = requests.get(rawUrl, headers=headers, allow_redirects=False,
                                   timeout=30)  # 一般提取文本的话，那就用text，如果是文件就content
            rawhtml.encoding = chardet.detect(rawhtml.content)['encoding']
            # print(rawhtml.url)
            print("状态码" + str(rawhtml.status_code))
            if rawhtml.status_code == 504:
                print(504)
                return
            print("页面的读取结果为")
            # print(rawhtml.text)
            if rawhtml.text.find('rollback') == 0:
                jsonString = rawhtml.text.split("rollback")[1]  # 把js提取出来就可以了
            else:
                jsonString = rawhtml.text
            print(jsonString)
            dicData = eval(jsonString)
            print(type(jsonString))
            print(jsonString)
            # print(dicData['data']['article_info'])
            print(len(dicData['data']['article_info']))
            if dicData['data'] == "":
                print("超过了最大页数了，跳出了就可以了")
                return
            urllist = []
            for one in dicData['data']['article_info']:
                # print(one['url'])
                print(one['url'].replace("\\", "/"))  # 还需要检查一下这个和之前的那种野蛮是不是一样的
                urllist.append(one['url'].replace("\\", "/"))
            return urllist
        except Exception as e:
            # print(e)
            return []

    def pageUrlMain(self, date=(date.today() + timedelta(days=-CRAWL_DELAY_DAY)).strftime("%Y-%m-%d") ):  # 写入url进入数据库，并且写入分类
        resultUrlDic = {}  # 写入数据库使用这个
        tempList = []
        themeList = ['news', 'ent', 'tech', 'auto', 'house', 'finance', 'sports']  # 一共有7个主题，其实不止这7个的
        for theme in themeList:
            print("第一个主题是")
            tempDList = []
            for i in range(1, 12):  # 一般是10页就很多的了。10页以内
                print("第" + str(i) + "页")
                responseList = self.getThemeUrl(theme, date, i)
                if len(responseList) == 0:
                    print("最大页数为" + str(i - 1) + "页")
                    break
                else:
                    tempList = tempList + responseList
                    tempDList += responseList
            resultUrlDic[theme] = tempDList
            print(resultUrlDic)
        tempList = set(tempList)
        count = 0
        print("列表的url数量有：" + str(len(tempList)))
        for key in resultUrlDic:
            count += len(resultUrlDic[key])
        print("url总共有" + str(count))

        print("这个是PageUrls内的提取到的url")
        # pprint(resultUrlDic)
        print(len(resultUrlDic))

        print("这个开始是list类型的结果")
        # print(tempList)

        pprint(tempList)


        # self.dbhelper.saveDicToMysql(resultUrlDic,date,"tengxun")   #参数，字典结果集，时间，分类,这儿是不需要写的。
        return list(tempList)  # 直接这儿去重后


class WangyiExpend:  # 这个是网易爬虫需要获得新闻页面的拓展的部分，直接构造成start_urls,再来做别的操作。
    def getRollUrlList(self,date=(date.today() + timedelta(days=-CRAWL_DELAY_DAY)).strftime("%Y-%m-%d") ):  #这个打开会是手机端的东西    #又重写了一遍了这个东西
        rollLatest = "http://news.163.com/latest/"  #这个就是默认新闻
        requestURL ="http://news.163.com/special/0001220O/news_json.js?0.3699326344116929"

        my_headers = [                       #这边为了得到直接的手机端的页面代码返回，直接使用手机ua
            'Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN',
            'Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Mobile Safari/537.36 Maxthon/3047',
            # 'Mozilla/5.0 (iPhone 84; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14G60 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
            'Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; STF-AL00 Build/HUAWEISTF-AL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.9 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; SM-C7000 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.2.948 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 7.0; STF-AL10 Build/HUAWEISTF-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/4G WebP/0.3.0 Pixel/1080']

        headers = {"User-Agent": random.choice(my_headers), 'Referer': "http://news.163.com/latest/"}  # 默认值

        try:
            rawhtml = requests.get(requestURL, headers=headers, allow_redirects=False,
                                   timeout=30)  # 一般提取文本的话，那就用text，如果是文件就content
            rawhtml.encoding = "GBK"  ##gbk>gb2312   使用这种方式尚且还有乱码的情况，部分乱码，那就是gbk可以修复
            # print(chardet.detect(rawhtml.content)['encoding'])
            if rawhtml.status_code == 504:
                print(504)
                return
            # print(rawhtml.url)
            print("状态码" + str(rawhtml.status_code))
            # print("页面的读取结果为")
            html = rawhtml.text

            result10=[]
            if html.find('"news":')!=-1:
                rawjsonString = html.split('"news":')[1].replace("};","")
                jsDic = eval("("+rawjsonString+")")
                for i in jsDic:
                    if len(i)!=0:
                        for content in i:
                            if content['p'].split(" ")[0]==date:   #这个是今天的
                                url = content['l']
                                if url.find("photoview")==-1:            #不是图片的写入这儿
                                    result10.append(content['l'])
                                else:
                                    pass

                # print("插入了"+str(len(result10)))
                print(result10)
                # self.saveListToMysql(result10, date)  # todo  这儿做了注释，不写入数据库，方便进行测试/

                return result10          #这个是返回前一天的所有的url链接放在这儿，大概200条以内，又变少了啊
        except Exception as e:
            print(e)
            return   #返回为空
if __name__ == '__main__':
    # 腾讯的获得新闻列表的模块测试
    # tengxun_expend =TengxunExpend()
    # tengxun_expend.pageUrlMain()

    # 网易的获得新闻的列表的模块测试
    wangyi_expend =WangyiExpend()
    print(wangyi_expend.getRollUrlList())  # 默认都是获得昨天的新闻。
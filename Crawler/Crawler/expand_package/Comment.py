# -*- coding: utf-8 -*

# 这个是收集评论的类
# todo 评论好像有问题，这边这儿的。
import time

import emoji

# from DBcontrol import DB
# from makebeautifulSoup import makeBS

# from NewsSenti.tengxun.DBcontrol import DB
# from NewsSenti.tengxun.makebeautifulSoup import makeBS
from Crawler.expand_package.DBcontrol import DB
from Crawler.expand_package.makebeautifulSoup import makeBS


class CommentCrawl(object):
    def __init__(self):
        self.dbHelper = DB()

    def changTimeToDate(self,dateString):
        timeStamp = dateString
        timeArray = time.localtime(timeStamp)
        print(timeArray)
        otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
        # print(otherStyleTime)
        return otherStyleTime


    def getNewsIdAndUrl(self):   #提取出新闻的id和url
        # dbHelper = DB()
        themeWord = ['car','technology','home','entertainment','house','finance','sports']  #类别新闻
        resultDic = {}
        sqlHead = "select News_id,url from newssentimentanalysis_"
        sqlTail = "news where Mcontent='未提取'"   # 记得更新了状态后要修改成已提取
        # 插入
        for theme in themeWord:
            print(sqlHead+theme+sqlTail)
            resultDic[theme] = self.dbHelper.__query__(sqlHead+theme+sqlTail)# 查询
        return resultDic  #返回格式{'car':[{'id':xx,'url':xx},.....,'home'...]

    def getAwriteCommentJson(self,id,url,theme):             #这个是评论专用的请求返回成字典的,theme 是方便找到表然后更新状态的。
        sqlHead = "update newssentimentanalysis_"
        sqlTail = "news set Mcontent='%s' and where url='%s '"   # 更新指定表内的评论状态词,需要只处理腾讯的吗

        sql = sqlHead+theme+sqlTail % ("已提取",url)  #这个是更新状态用的sql

        # 异常时一般是没有评论
        sqlERROR = sqlHead+theme+sqlTail % ("无评论",url)  # 如果发现没有


        time.sleep(0.5)
        cooker = makeBS()
        commentRawUrl = "http://coral.qq.com/article/"
        cmt_id = cooker.getCmt_id(url)  #去掉空格
        if cmt_id==None:
            return False  # 没有找到的话,那就是没评论啊
        if cmt_id.find("'")!=-1:
            cmt_id = cmt_id.replace("'","")
        else :
            cmt_id = cmt_id.strip()

        #这个用来拼接用到。
        try:
            allUrl = commentRawUrl + str(cmt_id) + "/comment/#"
            print(allUrl)
            responseDic = cooker.makeBSjson(allUrl)
            commentList = responseDic['data']['commentid']  # todo 不知道怎么回事调用不到这个评论的。
            # print(commentList)
            from pprint import pprint
            for comment in commentList:
                pprint(type(comment['id']))
                print(comment['id'])
                comment['content'] = emoji.demojize(comment['content'])      #过滤emoji
                comment['userinfo']['nick'] = emoji.demojize(comment['userinfo']['nick'])
                comment['time']=self.changTimeToDate(comment['time'])             #时间戳改成日期字符串
                print("新闻id "+ str(id))
                print("新闻的url是 "+ url)
                if self.dbHelper.classifyDBComment(url=url,id=id,comment=comment)  : #评论直接插入django表内的数据库,并且更新新闻评论状态.
                    print("更新成功")
                    self.dbHelper.__query__(sql)  # 这儿设置更新里面新闻的状态。
                else:
                    print("更新失败")
                    self.dbHelper.__query__(sqlERROR)   # 这儿设置更新里面新闻的状态。
                print("已经成功更新此条新闻 "+url+" "+theme)
                print("")
                return True
                #-----------------------这儿可以合成sql语句的话就可以执行插入的操作了。-----------------------
                # 通过url来合成插入的sql语句，DBcontrol的方法中来做这些东西
        except Exception as e:
            print("此条可能无评论，正在跳过")
            #  这儿需要插入无评论才可以。 todo
            # self.dbHelper.__query__(sqlERROR)  # 失败的话,更新成失败
            print(sqlERROR)     #更新成
            print(e)
            return False


    def getCommentMain(self):  # 这儿应该是提取出所有为提取的新闻，然后还要记得更新状态
        resultDic = self.getNewsIdAndUrl()  # 返回的是拼装好的含主题的list
        # from pprint import  pprint
        # pprint(resultDic)

        resultList = []
        count = 0
        for theme in resultDic:
            print("现在是",theme)
            for oneNews in resultDic[theme]:
                count+=1  #这个累加，然后如果是到了一定的数量那就休眠一下
                if count%100==0:  #每100条
                    time.sleep(15) #休息两分钟。

                print(oneNews)  #已经提取出来了
                print("获得commentjson")
                # 分类----------------------------------------更新原来的状态.----------------------------------------
                sql = ""
                sql2=""
                sqlHead = "update  newssentimentanalysis_"
                # 'update  newssentimentanalysis_homenews set Mcontent="无评论" where News_id=1'
                sqlTail = "news set Mcontent = '已提取' where News_id={}"
                sqlTailErr = "news set Mcontent = '无评论' where News_id={}"

                # 插入正文得分的sql

                # 这句就是更新tengxun表中的数据,用id

                if oneNews['url'].find('auto') != -1 or oneNews['url'].find('car') != -1 :  # 找到这个就是汽车,中间是表名
                    sql = sqlHead + "car" + sqlTail
                    sql2 = sqlHead + "car" + sqlTailErr
                    pass
                elif oneNews['url'].find('tech') != -1:  # 找到这个就是科技
                    sql = sqlHead + "technology" + sqlTail
                    sql2 = sqlHead + "technology" + sqlTailErr

                    pass
                elif oneNews['url'].find('news') != -1:  # 找到这个就是默认新闻
                    sql = sqlHead + "home" + sqlTail
                    sql2 = sqlHead + "home" + sqlTailErr

                    pass
                elif oneNews['url'].find('ent') != -1:  # 找到这个就是娱乐
                    sql = sqlHead + "entertainment" + sqlTail
                    sql2 = sqlHead + "entertainment" + sqlTailErr

                    pass
                elif oneNews['url'].find('house') != -1:  # 找到这个就是房产
                    sql = sqlHead + "house" + sqlTail
                    sql2 = sqlHead + "house" + sqlTailErr

                    pass
                elif oneNews['url'].find('finance') != -1:  # 找到这个就是经济
                    sql = sqlHead + "finance" + sqlTail
                    sql2 = sqlHead + "finance" + sqlTailErr

                    pass
                elif oneNews['url'].find('sports') != -1:  # 找到这个就是运动
                    sql = sqlHead + "sports" + sqlTail
                    sql2 = sqlHead + "sports" + sqlTailErr

                    pass
                else:
                    print("这边这种是网易的情况-归为默认新闻home中去")

                    sql = sqlHead + "home" + sqlTail
                    sql2 = sqlHead + "home" + sqlTailErr

                print(theme) # 分类
                if self.getAwriteCommentJson(id=oneNews['News_id'],url=oneNews['url'],theme=theme):   #逐条插入，进行，这个不需要返回
                    print("提取出评论")
                    print(sql.format(oneNews['News_id']))
                    self.dbHelper.__query__(sql.format(oneNews['News_id']))

                else:
                    print("cmt_id 提取失败")
                    print(sql2.format(oneNews['News_id']))
                    self.dbHelper.__query__(sql2.format(oneNews['News_id']))
                    print("更新无评论")

                print()

                # resultList.append(oneNews)   # 添加进入
        print("finish comments crawl！")

if __name__ == '__main__':
    commentC  = CommentCrawl()
    # print(commentC.getNewsIdAndUrl())
    # print(commentC.getCommentJson("http:////sports.qq.com//a//20190315//000008.htm",55))  #测试单个
    commentC.getCommentMain()  #测试主题从url中提取，url又可以合成。


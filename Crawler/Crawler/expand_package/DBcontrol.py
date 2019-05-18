# -*- coding: utf-8 -*

# 此处是使用非orm来操作数据库的简单池化操作的代码
# 2018/9/8 修改成使用连接池的方式来进行数据库的链接
# 需要导入如下的依赖库，如果没有，请 安装 pymysql ,DBUtils
# 提取返回数据的全部变成了返回字典类型
# 这个是连接数据库的东西,这次使用数据库连接池把，使用连接池可以避免反复的重新创建新连接

import traceback
from datetime import date, timedelta
import emoji
import pymysql as pymysql
import time
from DBUtils.PooledDB import PooledDB

# 这个是从配置文件（同级目录下）config.py中加载链接数据库的数据
# mysqlInfo 中格式如下放着就可以,也可以直接使用,把__init__函数中需要链接部分直接替换即可
# mysqlInfo = {
#     "host": '127.0.0.1',
#     "user": 'root',
#     "passwd": '123456',
#     "db": 'test',   #改同一个数据库了。
#     "port": 3306,
#     "charset": 'utf8'  #这个是数据库的配置文件
# }
# from .senti_dict_class import Senti_dict_class
from Crawler.expand_package.senti_dict import Senti_Text
from Crawler.settings import mysqlInfo


class DB:  

    __pool = None   #这个也是静态的属性

    def __init__(self):
        # 构造函数，创建数据库连接、游标，默认创建一个对象就获得一个连接，用完后就关闭就可以了
        self.coon = DB.getmysqlconn()  #这个是默认创建出来的东西
        self.cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)

    # 数据库连接池连接
    @staticmethod   # 这个是静态的方法可以直接调用的
    def getmysqlconn():  # 从连接池里面获得一个连接
        if DB.__pool is None:
            __pool = PooledDB(creator=pymysql, mincached=2, maxcached=20, host=mysqlInfo['host'],
                                  user=mysqlInfo['user'], passwd=mysqlInfo['passwd'], db=mysqlInfo['db'],
                                  port=mysqlInfo['port'], charset=mysqlInfo['charset'])
            # print(__pool)
        return __pool.connection()
        # 释放资源

    def dispose(self): #这儿只能断默认初始化的那个连接
        self.coon.close()
        self.cur.close()

# ---------------- 这儿开始写方法-----------------------
    def ifExists(self,webTitle):
        coon = DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "SELECT * FROM tengxun WHERE title='%s'and urlState='True';"
        #因为这儿没有加上try，catch，所以出问题
        try:
            cur.execute(sql%(webTitle))
        except Exception as e:
            print(e)
            print("函数ifExists出问题了，你检查一下")
            print(sql%(webTitle))
        rowNumber = cur.rowcount
        if rowNumber>0:
            return True
        else:
            return False


# ------- 下面可以日常的直接编写操作数据库的代码---------------


    def __query__(self,sql):  # 自定义查询,返回字典的类型
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)  # 这儿这个选项是设置返回结果为字典的类型，如果默认的话，那就是列表i
        # ----- 标准的查询模块 ---下面就是执行的部分
        try:
            cur.execute(sql)
            URLs = cur.fetchall()  # 返回数据的列表，可以设置返回的是字典
            # -----
            print(sql)
            print(cur.rowcount)
            coon.commit()


            return URLs
        except Exception as e:
            print(e)
            coon.rollback()
        finally:
            cur.close()
            coon.close()


  
    # 更新部分的例子，sql语句不同而已
    def updateById(self,id):
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        sql = "update tengxun set hadmix='True' where id = %d;" % int(id)   #就只是更新一下相应的url的状态就可以了
        try:  
            cur.execute(sql)
            # 提交
            coon.commit()
        except Exception as e:
            # 错误回滚
            print("更新出错")
            print(e)
            coon.rollback()
        finally:
            coon.commit() #提交这个事务
            cur.close()
            coon.close()
        

    # 插入的例子
    def insert(self,value): #这个是把网址先存到里面去url，这儿的意思是插入tengxun那个表
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "insert into testtable (value) values(%s)"
        try:
            cur.execute(sql,value)  # 这样来直接把值替换进行就可以,注意类型
            # 提交
            coon.commit()
        except Exception as e:
            # 错误回滚
            print(sql)
            print(e)
            coon.rollback()
        finally:
            coon.commit() #提交这个事务
            cur.close()
            coon.close()


    def insert(self,value): #这个是把网址先存到里面去url，这儿的意思是插入tengxun那个表
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "insert into tengxun (url) values(%s)"
        try:
            cur.execute(sql,value)  # 这样来直接把值替换进行就可以,注意类型
            # 提交
            coon.commit()
        except Exception as e:
            # 错误回滚
            print(sql)
            print(e)
            coon.rollback()
        finally:
            coon.commit() #提交这个事务
            cur.close()
            coon.close()


    # 更新的例子 todo 加上插入数据库的操作。把一个item传进来把 , 这个是可以统一使用的。
    def insertItem(self,item):
        '''
            url = scrapy.Field()
            urlState = scrapy.Field()
            title = scrapy.Field()
            Hcontent =  scrapy.Field()
            Tcontent = scrapy.Field()
            Acontent = scrapy.Field()
            newdate = scrapy.Field()
            fromWhere = scrapy.Field()
        :param item:  默认item是[] 列表内的，哪怕是一个元素也也是一样的。
        :return:
        '''
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "insert into tengxun (url,urlState,title,Hcontent,Tcontent,Acontent,newdate,fromWhere)" \
              " values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')".format(
            item['url'][0],item['urlState'][0],item['title'][0],item['Hcontent'][0],item['Tcontent'][0],
            item['Acontent'][0],item['newdate'][0],item['fromWhere'][0])

        try:
            print(sql)
            cur.execute(sql)  # 这样来直接把值替换进行就可以,注意类型
            # 提交
            coon.commit()
            print("插入数据库tengxun成功")
        except Exception as e:
            # 错误回滚
            print(sql)
            print(e)
            coon.rollback()
            # time.sleep(30)
        finally:
            coon.commit() #提交这个事务
            cur.close()
            coon.close()

    # ----------------------------------评论的数据库分类插入,传入新闻的url和id,commentDic <聚合的dic>
    def classifyDBComment(self,url,id,comment):
        print("开始分类整理")  #
        # print(comment['id'])
        sql = ""  #评论正文插入   m  nbvcbv
        sqlHead = "insert into newssentimentanalysis_"
        sqlTail = "comment  (NikeName,Comment,Date,News_id_id) values (%s,%s,%s,%s)"

        # 插入评论得分的sql
        sql2 = ""
        sql2Tail = "analysis_comment(Pos_Score,Neg_score,Sentiment,Comment_id_id,Date) values (%s,%s,%s,last_insert_id(),%s)"  # 这个我也知道

            # 这句就是更新新闻表中的数据,用id  newssentimentanalysis_carcomment
        sqlNews = ""
        sqlNewsHead = "update newssentimentanalysis_"
        sqlNewsTail = "news SET Mcontent='已提取' where News_id=%s"  #id是数字

        # 插入正文得
        # updateSql = "update tengxun SET hadmix='True' where id='%s' "  #Mcontent，这个字段用来“未提取”-》“已提取

        if url.find('auto') != -1:  # 找到这个就是汽车,中间是表名
            sql = sqlHead + "car" + sqlTail
            sql2 = sqlHead + "car" + sql2Tail
            sqlNews =sqlNewsHead+ "car"+ sqlNewsTail
            pass
        if url.find('tech') != -1:  # 找到这个就是科技
            sql = sqlHead + "technology" + sqlTail
            sql2 = sqlHead + "technology" + sql2Tail
            sqlNews =sqlNewsHead+ "technology"+ sqlNewsTail

        if url.find('news') != -1:  # 找到这个就是默认新闻
            sql = sqlHead + "home" + sqlTail
            sql2 = sqlHead + "home" + sql2Tail
            sqlNews =sqlNewsHead+ "home"+ sqlNewsTail


        if url.find('ent') != -1:  # 找到这个就是娱乐
            sql = sqlHead + "entertainment" + sqlTail
            sql2 = sqlHead + "entertainment" + sql2Tail
            sqlNews =sqlNewsHead+ "entertainment"+ sqlNewsTail

        if url.find('house') != -1:  # 找到这个就是房产
            sql = sqlHead + "house" + sqlTail
            sql2 = sqlHead + "house" + sql2Tail
            sqlNews =sqlNewsHead+ "house"+ sqlNewsTail

        if url.find('finance') != -1:  # 找到这个就是经济
            sql = sqlHead + "finance" + sqlTail
            sql2 = sqlHead + "finance" + sql2Tail
            sqlNews =sqlNewsHead+ "finance"+ sqlNewsTail

        if url.find('sports') != -1:  # 找到这个就是运动
            sql = sqlHead + "sports" + sqlTail
            sql2 = sqlHead + "sports" + sql2Tail
            sqlNews =sqlNewsHead+ "sports"+ sqlNewsTail

        else:
            pass  # 未能分类,也放到默认的那儿去吗。

            # --------------------------------获取得分----------------------------------
        # print(type(comment['id']))
        print(comment['content'])
        print(emoji.demojize(comment['userinfo']['nick']))

        print(url,str(id))  # 这儿也是没有做异常处理的。

        # senti_counter = Senti_dict_class()
        # pos_score, neg_score, SentiResult = .Senti_Text(text)
        pos_score, neg_score, SentiResult = Senti_Text(comment['content'])  # 这个是纯文本部分
        # pos_score, neg_score, SentiResult = Senti_Text(comment['content'])  # 这个是纯文本部分
        if SentiResult.find("[")!=-1:
            SentiResult = SentiResult.replact("[","")
        if SentiResult.find("]")!=-1:
            SentiResult = SentiResult.replact("]","")
        print(SentiResult)
        # 中立的情况好像是返回直接是0
        print(pos_score)
            # ---------------------------这边开始数据库插入相关操作-----------------------------
        coon = DB.getmysqlconn()                                                          # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        try:
            cur.execute(sql, (
             comment['userinfo']['nick'], comment['content'],comment['time'], id)) # 插入指定的表（分类）


            cur.execute(sql2, (
            pos_score, neg_score, SentiResult,comment['time']))  # 插入评分 ,加上了日期了  todo获得评分
            # print(sqlNews % int(id))
            id = str(id)

            cur.execute(sqlNews, (id))                            # 更新新闻的 Mcontent,这个是可以工作的啊

            coon.commit()
            return True
            # time.sleep()
        except Exception as e:
            print(pos_score)
            print(neg_score)
            print(SentiResult)
            # print(Tcontent)
                # 错误回滚
            print("事务回滚，跳过插入")
                # print(rowDic['id'])
            print(sql, (
            comment['userinfo']['nick'], comment['content'],comment['time'], id))

            print(id)
            print(type(id))
            print(sqlNews % (id))


            print(e)
            coon.rollback()
            traceback.print_exc()
            return False  # 提取评论失败的都不管.
        finally:
            coon.commit()  # 提交这个事务
            cur.close()
            coon.close()
            print("这条新闻的评论写入完毕")

    # 把tengxun表中的数据，计算评分，并且分类到django表中去
    def classifyDB(self):  #
        resultDic = self.__query__(  # todo 测试部分
            "select id,url,title,urlState,Hcontent,Mcontent,Tcontent,Acontent,newdate,fromWhere from tengxun where urlState='True' and hadmix='False'")
        print("开始分类整理")
        for rowDic in resultDic:
            # 插入分类新闻主表的sql
            sql = ""
            sqlHead = "insert into newssentimentanalysis_"
            sqlTail = "news (url,Title,UrlState,Hcontent,Mcontent,Tcontent,Acontent,Date,fromWhere) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

            # 插入正文得分的sql
            sql2 = ""
            sql2Tail = "analysis_news(Pos_Score,Neg_score,Sentiment,News_id_id,Date) values (%s,%s,%s,last_insert_id(),%s)"  # 这个是sql的

            # 这句就是更新tengxun表中的数据,用id
            updateSql = "update tengxun SET hadmix='True' where id='%s' "  # 这个是分类用的数据.

            if rowDic['url'].find('auto') != -1:  # 找到这个就是汽车,中间是表名
                sql = sqlHead + "car" + sqlTail
                sql2 = sqlHead + "car" + sql2Tail
                pass
            if rowDic['url'].find('tech') != -1:  # 找到这个就是科技
                sql = sqlHead + "technology" + sqlTail
                sql2 = sqlHead + "technology" + sql2Tail

                pass
            if rowDic['url'].find('news') != -1:  # 找到这个就是默认新闻
                sql = sqlHead + "home" + sqlTail
                sql2 = sqlHead + "home" + sql2Tail

                pass
            if rowDic['url'].find('ent') != -1:  # 找到这个就是娱乐
                sql = sqlHead + "entertainment" + sqlTail
                sql2 = sqlHead + "entertainment" + sql2Tail

                pass
            if rowDic['url'].find('house') != -1:  # 找到这个就是房产
                sql = sqlHead + "house" + sqlTail
                sql2 = sqlHead + "house" + sql2Tail

                pass
            if rowDic['url'].find('finance') != -1:  # 找到这个就是经济
                sql = sqlHead + "finance" + sqlTail
                sql2 = sqlHead + "finance" + sql2Tail

                pass
            if rowDic['url'].find('sports') != -1:  # 找到这个就是运动
                sql = sqlHead + "sports" + sqlTail
                sql2 = sqlHead + "sports" + sql2Tail

                pass
            else:
                print("这边这种是网易的情况-归为默认新闻home中去")

                sql = sqlHead + "home" + sqlTail
                sql2 = sqlHead + "home" + sql2Tail

                pass  # 未能分类,也放到默认的那儿去吗。  #

            # --------------------------------获取得分----------------------------------
            print("Tcontent长度")
            print(len(rowDic['Tcontent']))
            pos_score, neg_score, SentiResult = "", "", ""

            # senti_counter = Senti_dict_class()
            pos_score, neg_score, SentiResult = Senti_Text(rowDic['Tcontent'])
            # pos_score, neg_score, SentiResult = senti_counter.Senti_Text(rowDic['Tcontent'])  # 这个是纯文本部分

            # todo 进行分数写入和的部分


            # pos_score, neg_score, SentiResult = Senti_Sentence(rowDic['Tcontent'])  #这个是纯文本部分

            print("分类时候写入分数检查")
            print()

            # print(rowDic['Tcontent'])
            # print()
            print(sql % (
                rowDic['url'], rowDic['title'], True, rowDic['Hcontent'], '未提取', rowDic['Tcontent'], rowDic['Acontent'],
                rowDic['newdate'], rowDic['fromWhere']
            ))
            print(pos_score)
            print(neg_score)
            print(SentiResult)

            # ---------------------------这边开始数据库插入相关操作-----------------------------

            coon = DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
            cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
            # print(rowDic['url'])
            # print(rowDic['title'])
            # print(rowDic['Hcontent'])
            # print('未提取')
            # print(rowDic['Tcontent'])
            # print(rowDic['Acontent'])
            # print(rowDic['newdate'])
            # print(rowDic['fromWhere'])

            # print((sql %(
            #                     rowDic['url'],rowDic['title'],"True",rowDic['Hcontent'],'未提取',rowDic['Tcontent'],rowDic['Acontent'],rowDic['newdate'],rowDic['fromWhere']
            #                 )
            #                 ))

            try:  # 三个一起操作，很多麻烦事情的。可以，这样操作也是可以的。
                cur.execute(sql,
                            (
                                rowDic['url'], rowDic['title'], True, rowDic['Hcontent'], '未提取', rowDic['Tcontent'],
                                rowDic['Acontent'], rowDic['newdate'], rowDic['fromWhere']
                            )
                            )  # 插入指定的表（分类）

                print("插入成功才用得上这个的把。")  # 无法提取到这个的。在写一次查询把。
                # print(cur.lastrowid())      # 上一个插入的id是，还真是有，那就直接返回过来就可以了
                # print(type(cur.lastrowid()))   # 上一个插入的id是，还真是有，那就直接返回过来就可以了

                cur.execute(sql2, (pos_score, neg_score, SentiResult, rowDic['newdate']))  # 插入评分   todo获得评分
                cur.execute(updateSql, (rowDic['id']))  # 更新tengxun hadmix,这个是可以工作的啊
                # 提交
                coon.commit()

            except Exception as e:
                # 错误回滚
                print("事务回滚，跳过插入")
                # print(rowDic['id'])
                # print(sql%(rowDic['url'],rowDic['title'],True,rowDic['Hcontent'],'未使用',rowDic['Tcontent'],rowDic['Acontent'],rowDic['newdate'],rowDic['fromWhere']))
                print(e)
                coon.rollback()
                traceback.print_exc()

            finally:
                # print("插入成功")
                coon.commit()  # 提交这个事务
                cur.close()
                coon.close()
        print("今天的量分完了")




if __name__ == "__main__":  # 下面都是用来测试用的。

    chak = DB()
    # chak.classifyDB()
    # chak. 测试用调用
    chak.__query__("update  newssentimentanalysis_carnews set Mcontent = '无评论' where News_id=4")



    print("DB finish!")





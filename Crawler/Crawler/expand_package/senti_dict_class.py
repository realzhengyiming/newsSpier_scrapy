#-*- coding:utf8 -*-
import jieba
import numpy as np
import re
import jieba
#打开词典文件，返回列表


class Senti_dict_class:
    def __init__(self):
        pass

        # self.deny_word = self.open_dict(Dict='否定词', path=r'./Sent_Dict/')
        # self.posdict = self.open_dict(Dict='positive', path=r'./Sent_Dict/')
        # self.negdict = self.open_dict(Dict='negative', path=r'./Sent_Dict/')
        # self.degree_word = self.open_dict(Dict='程度级别词语', path=r'./Sent_Dict/')

        self.deny_word = self.open_file_as_text('./Sent_Dict/否定词.txt')
        self.posdict = self.open_file_as_text('./Sent_Dict/positive.txt')
        self.negdict = self.open_file_as_text('./Sent_Dict/negative.txt')
        self.degree_word = self.open_file_as_text('./Sent_Dict/程度级别词语.txt')


        self.mostdict = self.degree_word[self.degree_word.index('extreme') + 1: self.degree_word.index('very')]  # 权重4，即在情感词前乘以4
        self.verydict = self.degree_word[self.degree_word.index('very') + 1: self.degree_word.index('more')]  # 权重3
        self.moredict = self.degree_word[self.degree_word.index('more') + 1: self.degree_word.index('ish')]  # 权重2
        self.ishdict = self.degree_word[self.degree_word.index('ish') + 1: self.degree_word.index('last')]  # 权重0.5


    def open_file_as_text(self,filename):
        dict = []
        with open(filename, encoding='utf-8') as f:
            # print(f.read())
            dict=f.readlines()
        new = []
        for word in dict:
            new.append(word.replace("\n",""))
        print(new)
        return new

    def open_dict(self,Dict = 'name', path=r'Sent_Dict/'):
        path = path + '%s.txt' % Dict
        dictionary = open(path, 'r', encoding='utf-8')
        dict = []
        for word in dictionary:
            word = word.strip('\n')
            dict.append(word)
        return dict

    def judgeodd(self,num):
        if (num % 2) == 0:
            return 'even'
        else:
            return 'odd'






    def sentiment_score_list(self,dataset):
        seg_sentence = dataset.split(' 。')
        count1 = []
        count2 = []
        for sen in seg_sentence: #循环遍历每一个评论
            segtmp = jieba.lcut(sen, cut_all=False)  #把句子进行分词，以列表的形式返回
            i = 0 #记录扫描到的词的位置
            a = 0 #记录情感词的位置
            poscount = 0 #积极词的第一次分值
            poscount2 = 0 #积极词反转后的分值
            poscount3 = 0 #积极词的最后分值（包括叹号的分值）
            negcount = 0
            negcount2 = 0
            negcount3 = 0
            for word in segtmp:
                if word in self.posdict:  # 判断词语是否是情感词
                    poscount += 1
                    c = 0
                    for w in segtmp[a:i]:  # 扫描情感词前的程度词
                        if w in self.mostdict:
                            poscount *= 4.0
                        elif w in self.verydict:
                            poscount *= 3.0
                        elif w in self.moredict:
                            poscount *= 2.0
                        elif w in self.ishdict:
                            poscount *= 0.5
                        elif w in self.deny_word:
                            c += 1
                    if self.judgeodd(c) == 'odd':  # 扫描情感词前的否定词数
                        poscount *= -1.0
                        poscount2 += poscount
                        poscount = 0
                        poscount3 = poscount + poscount2 + poscount3
                        poscount2 = 0
                    else:
                        poscount3 = poscount + poscount2 + poscount3
                        poscount = 0
                    a = i + 1  # 情感词的位置变化

                elif word in self.negdict:  # 消极情感的分析，与上面一致
                    negcount += 1
                    d = 0
                    for w in segtmp[a:i]:
                        if w in self.mostdict:
                            negcount *= 4.0
                        elif w in self.verydict:
                            negcount *= 3.0
                        elif w in self.moredict:
                            negcount *= 2.0
                        elif w in self.ishdict:
                            negcount *= 0.5
                        elif w in self.degree_word:
                            d += 1
                    if self.judgeodd(d) == 'odd':
                        negcount *= -1.0
                        negcount2 += negcount
                        negcount = 0
                        negcount3 = negcount + negcount2 + negcount3
                        negcount2 = 0
                    else:
                        negcount3 = negcount + negcount2 + negcount3
                        negcount = 0
                    a = i + 1
                elif word == '！' or word == '!':  ##判断句子是否有感叹号
                    for w2 in segtmp[::-1]:  # 扫描感叹号前的情感词，发现后权值+2，然后退出循环
                        if w2 in self.posdict or self.negdict:
                            poscount3 += 2
                            negcount3 += 2
                            break
                i += 1 # 扫描词位置前移


                # 以下是防止出现负数的情况
                pos_count = 0
                neg_count = 0
                if poscount3 < 0 and negcount3 > 0:
                    neg_count += negcount3 - poscount3
                    pos_count = 0
                elif negcount3 < 0 and poscount3 > 0:
                    pos_count = poscount3 - negcount3
                    neg_count = 0
                elif poscount3 < 0 and negcount3 < 0:
                    neg_count = -poscount3
                    pos_count = -negcount3
                else:
                    pos_count = poscount3
                    neg_count = negcount3

                count1.append([pos_count, neg_count])
            count2.append(count1)
            count1 = []

        return count2

    def sentiment_score(self,senti_score_list):
        score = []
        for review in senti_score_list:
            score_array = np.array(review)
            Pos = np.sum(score_array[:, 0])
            Neg = np.sum(score_array[:, 1])
            AvgPos = np.mean(score_array[:, 0])
            AvgPos = float('%.1f'%AvgPos)
            AvgNeg = np.mean(score_array[:, 1])
            AvgNeg = float('%.1f'%AvgNeg)
            StdPos = np.std(score_array[:, 0])
            StdPos = float('%.1f'%StdPos)
            StdNeg = np.std(score_array[:, 1])
            StdNeg = float('%.1f'%StdNeg)
            score.append([Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg])
        return score


    def Senti_Sentence(self,word):
        if word == '':
            return 0,0,'NEU'
        else:
            result = self.sentiment_score(self.sentiment_score_list(str(word)))  # 情感分析
            pos_score = result[0][0]
            neg_score = result[0][1]
            if pos_score == neg_score:
                SentiResult='NEU'
            elif pos_score > neg_score:
                SentiResult='POS'
            else:
                SentiResult='NEG'
            #print(pos_score,neg_score,SentiResult)
            return float(pos_score),float(neg_score),SentiResult

    def Senti_Text(self,text):
        if text == '':
            return 0,0,'NEU'
        else:
            text = str(text)
            seg_sentence = re.split('。|！|？|……|,',text)
            print(seg_sentence)
            pos_sum=0
            neg_sum=0
            sen_num=0
            for sentence in seg_sentence:
                if sentence != '':
                    pos,neg,res=self.Senti_Sentence(sentence)
                    pos_sum+=pos
                    neg_sum+=neg
                    sen_num+=1
                else:
                    pass
            print('句子数：',sen_num)
            try:
                pos_score = pos_sum/sen_num
                neg_score = neg_sum/sen_num
                if pos_score == neg_score:
                    SentiResult='NEU'
                elif pos_score > neg_score:
                    SentiResult='POS'
                else:
                    SentiResult='NEG'
                #print(pos_score,neg_score,SentiResult)
                return float(pos_score),float(neg_score),SentiResult
            except Exception as e :  #
                print(e)
                return 0,0,'NEU'



if  __name__=="__main__":
    #data = '你就是个王八蛋，混账玩意!你们的手机真不好用！非常生气，我非常郁闷！！！！'
    #data2= '我好开心啊，非常非常非常高兴！今天我得了一百分，我很兴奋开心，愉快，开心'
    text='腾讯汽车 站]编辑从深圳市大兴观澜丰田了解到，卡罗拉双擎最高优惠0.30万元，促销时间为2019年03月01日--2019年03月03日， 欢迎有意向的朋友到店试乘试驾。卡罗拉双擎外观卡罗拉双擎内饰卡罗拉双擎细节版权声明：本文系腾讯汽车独家稿件，版权为腾讯汽车所有。文章内的价格为编辑在车市第一线真实采集到的当日价格，由于汽车价格变化莫测，同时此价格只是个体经销商的行为，所以价格仅供参考使用。'
    # print(sentiment_score_list(data))
    # print(sentiment_score(sentiment_score_list(data)))
    #print(sentiment_score(sentiment_score_list(data2)))
    senti_counter = Senti_dict_class()
    pos_score,neg_score,SentiResult=senti_counter.Senti_Text(text)
    print( pos_score,neg_score,SentiResult)

    # senti_counter.open_file_as_text("Sent_Dict/否定词.txt")


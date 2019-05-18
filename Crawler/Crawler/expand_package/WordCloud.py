# -*- coding: utf-8 -*

from wordcloud import WordCloud
import PIL.Image as image
import numpy as np
import jieba
import datetime
import os
import time

from Crawler.settings import IMAGES_STORE, WORDCLOUD_STORE

Yesterday = (datetime.datetime.now()-datetime.timedelta(days=2)).strftime('%Y-%m-%d')#昨天

def trans_CN(text):
	#中文要进行分词，不像英文自动有空格
	wordlist = jieba.cut(text)
	result = ' '.join(wordlist)
	return result


def Gen_WordCloud(text,Newsid):
	#输入：text文章内容，Newsid文章的id号
	#输出：image_path对应词云图片的路径
	text = trans_CN(text)#分词
	#mask = np.array(image.open('./static/images/cloud.png'))#如果要把词云形状弄成特定图形要用该语句
	wordcloud = WordCloud(
		#mask=mask,
		font_path = "C:\Windows\Fonts\simhei.ttf", #加载中文字体
		background_color='white', #背景色
		max_words=2000,#允许最大词汇
		#max_font_size=60 #最大号字体
	).generate(text)
	
	image_produce = wordcloud.to_image()
	name = str(Newsid)+".png" #构造温江名
	# path = "../../static/images/WordCloud/" #保存文件夹
	path = WORDCLOUD_STORE
	if not os.path.exists(path):
		os.makedirs(path)
	save_path =path+name #保存的完整路径 这个地址也是创建到爬虫项目的外面，刚好，目录结构不变的情况下。
	print(save_path)
	wordcloud.to_file(save_path) #保存词云
	img_path=save_path+name #对应的要传给<img>标签的路径
	#print("save to :",save_path)
	#image_produce.show()
	print("生成词云成功了！")
	return img_path

if __name__=="__main__":
	Newsid="shitshit"
	text='近日，上汽大通官方公布了全新MPV车型G20的最新官图，从此次公布的官图中不难看出，大通G20在外形轮廓上沿用了家族式设计。大灯采用了全LED光源，造型极具科技感。内饰中控区采用了悬浮式设计，营造出了更多的储物空间。据悉，大通G20将在2019上海车展期间正式亮相。从官图细节中可以看出，大通G20的前脸设计相比G10车型焕然一新。不规则形状的大灯和硕大的进气格栅相连接，其大灯内部结构也更加复杂，采用全LED光源。侧面轮廓上，大通G20采用了悬浮式车窗设计。尾灯同样采用全LED光源，两侧尾灯之间采用镀铬条相连，尾部采用字母logo居中的形式，而非图形logo。内饰部分，厂方着重强调了悬浮式中控设计。从官图中可以看出，大通G20采用了旋钮式换挡操作，换挡旋钮四周集成了众多驾驶辅助功能，视觉效果上具备更强的科技感。而悬浮式设计则为底部营造了更大的储物空间，便于放置乘客带上车的手包或其它物品。目前，官方暂未透露新车将会搭载哪款动力总成。根据推测，大通G20有望搭载2.0T汽油发动机和1.9T柴油发动机，预计在2019年上海车展期间正式亮相。'
	Gen_WordCloud(text,Newsid)
# newsSpider  scrapy
故名思意，这个就是一个新闻的爬虫，目前这个项目是用来练习scrapy框架的爬虫的地方。目前这个项目是一边学习一边的进行更新的，现在是用来爬取新浪新闻的，  

## xinlanggundong  (练习时的部分项目 🙃 下面的才是完整版本）
这儿是新浪新闻滚动新闻的测试项目部分  

## Crawler （比较完整 😀 ）  
比较完整的，爬取 腾讯 、网易 、新浪 新闻的scrap爬虫项目。  
### 功能：  
+ 服务器上运行可以设定定时爬取  
+ 管道部分写的是自定义写入自己定义的mysql的样式，具体使用可以在settings中启用或者停用或者自定义
+ 里面是spiders/文件夹下三个平台的爬虫可以一同进行爬取工作，
+ 对腾讯、网易、新浪新闻中的正文和图片进行本地化爬取。
+ 并且管道中有对每篇新闻生成对应的词云图片

### 使用方法:  
+ 1.安装scrapy 环境，建议conda配置
+ 2.git clone https://github.com/realzhengyiming/newsSpier_scrapy.git
+ 3.```cd Crawler```   
+ 4.```python Together_Crawl.py``` 一次性跑三个爬虫，包括腾讯、网易、新浪
+ 5.```python togetherCrawl_scheduling.py``` 一次性跑三个爬虫，包括腾讯、网易、新浪（定时，时间设置先在settings.py中设置）
    + 设置settings.py 中``` CRAWLALL_RUN_TIME="XX:XX" 24小时制 ```
    + 如果是linux上定时跑，可以 ```nohup python togetherCrawl_scheduling.py```  
+ 6. ```python tengxunMain.py```  只爬取腾讯爬虫的部分
+ 7. ```python wangyiMain.py```  只爬取网易新闻爬虫的部分  
+ 8.```python xinlangMain.py```  只爬取新浪爬虫的部分
+ 9. 重写了命令，可以直接scrapy crawlall 进行三个爬虫的同时爬取（同理默认scrapy crawl tengxun 这样也是可以的）   

### 更多设置  
+ 6.新闻中的图片需要下载请在settings.py 中 设置，如``` IMAGES_STORE = "../static/images/"   ```(此处使用相对路径）  
    + ```DOWMLOAD_IMG_IN_ACONTENT = False ```   开启或者关闭把新闻中的图片本地化操作。 
+ 7.开关词云的生成，settings.py 中设置  
    + ``` MAKE_WORDCLOUD_STORE = True ``` 默认开启词云
    + ``` WORDCLOUD_STORE = "../static/images/WordCloud/" ``` 设置词云的生成地址，默认是相对路径，项目外同级目录

### 注意🎃  
因为我这个项目是另一个完整项目的一部分， 另一个完整项目是django+scrapy 的新闻的情感分析平台， 这是scrapy用来做数据爬取入库操作的。  

所以这儿的管道做的操作比较多，除了本地化图片和新闻正文，还有生成词云，甚至还有调用简单词频的方法进行情感分析的操作后才写入数据库的管道做的操作比较多，
除了本地化图片和新闻正文，还有生成词云，甚至还有调用简单词频的方法进行情感分析的操作后才写入数据库（django 数据库），所以使用的时候可以根据这个来改，去掉不需要的功能。



# todo
练习中待做的事情。
+ 设置UA  (👌)
+ 代理，类似ua  (👌) 
+ 设置请求延迟 (👌)  
    + settings 中 DOWNLOAD_DELAY (👌)  
+ 重写请求，使用 selenuim + chrome 无头模式组合来使用做动态爬取  (👌)   
+ 提取下一页后继续爬取  (👌)  
+ 可以爬取新浪新闻滚动页面了(默认设置成爬取前一天的，目前只能纯文本) (👌)  
+ 可以爬取新浪新闻滚动页面了(默认设置成爬取前一天的，结合图片和纯文本) (👌)  
+ 使用chrome+ selenuim 的时候下载图片前的设置referer 
+ 如果上面那条不太好用，也可以考虑 使用 requests-html 这个比较新的可以解析动态的库来进行合并。
+ 自定义下载媒体的图片 (👌)  
+ 链接把数据写入mongdb 或者  别的数据库mysql  (👌)  







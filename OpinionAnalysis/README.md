OpinionAnalysis
===============

Opinion Analysis 舆情分析系统


###功能

1. 抓取代理、多线程、自动重试
2. 通过代理抓取微博内容(新浪微博、和讯微博）
3. 通过代理抓取新闻（百度新闻、360新闻）
4. 将得到的结果进行数据格式统一化，并将格式统一的数据合并
5. 使用布隆过滤器进行结果去重[bloomfilter-redis](https://github.com/xupeng/bloomfilter-redis)
6. 文本情感分析（使用[snownlp](https://github.com/isnowfy/snownlp)）

###相关资料：

[用python爬虫抓站的一些技巧总结](http://www.pythonclub.org/python-network-application/observer-spider) 入门的时候看一下增加思路，参考了其中的GZIP压缩等，

[AllWeiboCrawler](https://github.com/paramiao/AllWeiboCrawler) 其中的新浪微博还能参考，和讯微博已经不能使用里面的方法了，我重写了。腾讯微博没发现多少有用的，所以没写，后续如果需要可以加上。

[Python实现Bloom filter](http://blog.csdn.net/pirage/article/details/8878846) 说理论的，其实这东西最开始是在数学之美里面看到的，没想到居然被我用上了，哈哈。具体项目中使用了Redis存放数据的版本，在测试过程中，我也找了一份用mmap映射到文件的版本，不过测试之后发现不能持久化，每次重新加载数据，之前的采集记录是不能被保存的，所以后来想到用REDIS，看了一下，有人已经做了，MIT协议，果断COPY。

[文本情感分析](http://21sq.org/?p=588) 看一下，来个思路先

[Naive Bayes 算法（NB算法）  ](http://dayu9.blog.163.com/blog/static/18628907920114135413342/)推荐这个，简单易懂，具体这个我也是在SNOWNLP里面看到的，所以研究了一下，发现确实用来做分类挺简单。。测试之后发现也还能接受，暂时就用他了。


[算法杂货铺——分类算法之朴素贝叶斯分类(Naive Bayesian classification)](http://www.cnblogs.com/leoo2sk/archive/2010/09/17/naive-bayesian-classifier.html)



###一些说明

关于爬虫的分析：打开CHROME，模拟手机，去各种手机版本的分析各种AJAX接口，直接找可用的API，这样就不用再麻烦的提取HTML。。各种整了。

关于布隆过滤器、其实就是几个哈希同时使用，然后有极小概率会出错，不过完全可以接受

关于情感分析，当然还有很多其他方式，如果有兴趣可以一起讨论,这里用最简单现成偷懒的办法COPY了别人的。：）


PS：
我刚学Python，不要吐槽!
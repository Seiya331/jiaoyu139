#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json

sys.path.append('../bloomfilter-redis')
sys.path.append('../snownlp/snownlp')

from multiprocessing.dummy import Pool as ThreadPool
import redis

from . import weibo
from . import news
from . import forum
from . import analysis
from . import proxy
from . import db
from . import logger
from bloomfilter import BloomFilter


class Opinion(object):
    def __init__(self, keywords):
        """

        :param keyword:
        :return:
        """
        # 加载代理配置
        proxy.load()

        self.logger = logger.get('opinion.init')
        self.config = self.load()

        #可以加载设置文件
        self.source = []
        for i in keywords['weibo']:
            #微博数据源
            self.source.append(weibo.WeiboCrawler(i))
            self.source.append(weibo.HexunCrawler(i))

        for i in keywords['news']:
            #新闻数据源
            self.source.append(news.BaiduNewsCrawler(i))
            self.source.append(news.So360NewsCrawler(i))
            self.source.append(news.SogouWenCrawler(i))
            self.source.append(news.XinBaoNewsCrawler(i))
            self.source.append(news.TaiZhouNewsCrawler(i))
            self.source.append(news.AnHuiNewsCrawler(i))
            self.source.append(news.PeopleNewsCrawler(i))
            self.source.append(news.EC100NewsCrawler(i))
            self.source.append(news.NenNewsCrawler(i))
            self.source.append(news.YcNewsCrawler(i))
            self.source.append(news.IKanChaiCrawler(i))
            self.source.append(news.HeXunNewsCrawler(i))
            self.source.append(news.EbrunNewsCrawler(i))
            self.source.append(news.JIA365Crawler(i))
            self.source.append(news.EC100NewsCrawler(i))
            # #论坛博客数据#
            self.source.append(forum.ZuanKe8Crawler(i))
            self.source.append(forum.DAYOOCrawler(i))
            #self.source.append(forum.WY163Crawler(i))
            self.source.append(forum.G8F8Crawler(i))
            self.source.append(forum.TouSuCrawler(i))
            self.source.append(forum.SinaBlogCrawler(i))
            self.source.append(forum.MAMACrawler(i))
            self.source.append(forum.IfengCrawler(i))
            self.source.append(forum.CCTVCrawler(i))
            self.source.append(forum.TaoBaoBBSCrawler(i))

        bloom = BloomFilter(connection=redis.Redis(host=self.config['redis']['host'],
                                                   port=self.config['redis']['port'],
                                                   db=self.config['redis']['db']),
                            bitvector_key=self.config['bloom']['key'],
                            n=self.config['bloom']['size'],
                            k=self.config['bloom']['k'])
        #分析模块
        self.analysis = analysis.Analysis(bloom)

        #数据库模块
        self.db = db.MysqlDB(
            host=self.config['mysql']['host'],
            user=self.config['mysql']['user'],
            passwd=self.config['mysql']['pass'],
            port=self.config['mysql']['port'],
            db=self.config['mysql']['db'],
            table=self.config['mysql']['table'],
        )

    def read(self, obj):
        """

        :param obj:
        :return:
        """
        result = obj.read()

        # 如果是微博，考虑到内容比较多，每次读取两页数据
        if isinstance(obj, weibo.WeiboCrawler):
            result.extend(obj.read())
        return result

    def get(self):
        """

        :return:
        """
        pool = ThreadPool(4)
        result = pool.map(self.read, self.source)
        pool.close()
        pool.join()

        items = []
        for i in result:
            # if i is not None or i is not False:
            items.extend(i)

        result = self.analysis.start(items)

        self.db.add(result)

        return result

    def test(self, index=0):
        items = self.read(self.source[index])
        return self.analysis.start(items)


    def load(self):
        """
        读取配置文件
        :return:
        """
        filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json'))
        try:
            f = open(filename, 'r')
            return json.load(f)
        except Exception as e:
            self.logger.debug('加载配置文件 %s 失败！%s' % (filename, e))
            return None
        except:
            raise

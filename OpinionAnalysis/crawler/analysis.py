#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'MLS'


from multiprocessing.dummy import Pool as ThreadPool
# from pybloomfilter import BloomFilter
from snownlp.snownlp import SnowNLP
from . import logger



class Analysis(object):
    """

    """
    def __init__(self,bloom):
        self.POSITIVE_THRESHOLD = 0.6
        self.NEUTRAL_THRESHOLD = 0.4
        self.NEGATIVE_THRESHOLD = 0.2

        # import os
        # file = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','tmp','item.bloom'))
        # self.bf = BloomFilter(50000000,0.01,file)
        self.bf = bloom
        self.logger = logger.get('opinion.crawler.analysis')

    def check(self,item):
        """

        :param list:
        :return:
        """
        #如果数据重复
        if not item or not item['text_content']:
            self.logger.debug('待分析的内容为空' )
            return None
        if item['unique_identify'] in self.bf:
            self.logger.debug('成功检测到重复内容%s' % item['unique_identify'] )
            return None
        #加入过滤列表
        self.bf.add(item['unique_identify'])


        nlp = SnowNLP(item['text_content'])
        prob = nlp.sentiments
        item['prob'] = "%.10f" % prob
        if prob > self.NEUTRAL_THRESHOLD:
            item['sentiment'] = 2
        elif prob <= self.POSITIVE_THRESHOLD:
            item['sentiment'] = 0
        else:
            item['sentiment'] = 1
        return item
        #正面，都累积以便修正结果
        # #负面情感，可以修正
        # if prob <= self.POSITIVE_THRESHOLD:
        #     try:
        #         item['title'] = item['title'].encode('utf-8','ignore')
        #         item['summary'] = item['summary'].encode('utf-8','ignore')
        #         item['author'] = item['author'].encode('utf-8','ignore')
        #     except Exception,e:
        #         self.logger.error('check转换 %s 编码出错！%s' % (item['title'],e) )
        #
        #     item['prob'] = "%.10f" % prob
        #     if prob > self.NEUTRAL_THRESHOLD:
        #         item['sentiment'] = 2
        #     elif prob <= self.POSITIVE_THRESHOLD:
        #         item['sentiment'] = 0
        #     else:
        #         item['sentiment'] = 1
        #     return item
        # else:
        #     return None

    def start(self,list):
        result = []
        for i in list:
            m = self.check(i)
            if m is not None:
                result.append(m)
        return result
        # pool = ThreadPool(8)
        # result = pool.map(self.check, list)
        # pool.close()
        # pool.join()
        # return [m for m in result if m is not None]

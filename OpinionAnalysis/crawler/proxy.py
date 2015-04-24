#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

json序列化参考：http://sebug.net/paper/books/dive-into-python3/table-of-contents.html#serializing

功能：每隔指定时间自动更新代理列表

支持多线程验证代理速度

"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import urllib2
import re
import json
import time
import random
import os
from multiprocessing.dummy import Pool as ThreadPool

from . import logger



class Proxy(object):
    def __init__(self):
        """

        :return:
        """
        # 提取正则
        self.extract_pattern = ur'<td></td>\s*?<td>.*?</td>\s*?<td>(((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?))</td>\s*?<td>(\d{2,4}?)</td>.*?(HTTPS?)<\/td>'
        #代理的配置文件名
        self.filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','config', 'proxy.json'))
        # 刷新间隔一小时更新一次代理
        self.refresh_interval = 3600
        # 抓取代理的地址
        self.proxy_site = 'http://www.xici.net.co/nn'
        #检测使用的地址
        self.test_url = 'http://www.baidu.com'
        #请求超时时间
        self.timeout = 10

        self.logger = logger.get('opinion.crawler.Proxy')

    def load(self, type='http', refresh=False):

        # type对应类型的代理列表 支持http、https
        config = self.read()
        if config is None:
            config = {'update_time': 0, 'http': [], 'https': []}

        now = int(time.time())
        # 跟上次更新代理列表的时间间隔
        interval = now - config['update_time']

        # 需要刷新代理列表
        if not config[type] or interval > self.refresh_interval or refresh == True:
            config['http'], config['https'] = self.crawler()
            config['update_time'] = now
            self.refresh(config)

        return config[type]

    def refresh(self, config=None):
        """
        刷新配置中的无效代理
        :param config:
        :return:
        """
        if config is None:
            config = self.read()
        # 刷新无效代理
        if config['http']:
            pool = ThreadPool(8)
            result = pool.map(self.check, config['http'])
            config['http'] = [http for http in result if http is not None]
            pool.close()
            pool.join()
            self.save(config)


    def crawler(self, retry=3):
        """
        抓取代理列表
        :param retry:
        :return:
        """
        self.logger.debug(u'开始更新代理列表')
        proxies = {'http': [], 'https': []}

        # 即使抓取代理都使用代理，有点恶心 O(∩_∩)O哈哈~
        config = self.read()
        if config is not None and config['http']:
            http = random.choice(config['http'])
            self.logger.debug(u'使用代理 %s 抓取代理!' % http)
            proxy_handler = urllib2.ProxyHandler({'http': http})
            opener = urllib2.build_opener(proxy_handler)
            urllib2.install_opener(opener)
        else:
            self.logger.debug(u'直连抓取代理!')

        #抓取该代理站的代理IP
        try:
            #5秒超时
            html = urllib2.urlopen(self.proxy_site, timeout=self.timeout).read()
            #提取代理信息
            regex = re.compile(self.extract_pattern, re.MULTILINE | re.DOTALL)
            for match in re.findall(regex, html):
                ##分开http和https
                proxies[match[5].lower()].append(u'%s://%s:%s' % (match[5].lower(), match[0], match[4]))
            self.logger.debug(u'更新代理列表成功!')
            return proxies['http'], proxies['https']

        except Exception as e:
            self.logger.debug(u'抓取%s代理列表出错，原因：%s，重试次数%s' % (self.proxy_site, e, retry ))
            #超时的话自动重试
            if retry > 0:
                return self.crawler(retry - 1)
            return [], []
        except:
            self.logger.debug(u'proxy.crawler出现未知错误！')
            raise



    def read(self):
        """
        读取代理的配置文件
        :return:
        """
        try:
            f = open(self.filename, 'r')
            return json.load(f)
        except Exception as e:
            self.logger.debug('加载', self.filename, '失败！', e)
            return None
        except:
            raise

    def save(self, data):
        """
        保存代理到文件
        :param data:
        :return:
        """
        try:
            f = open(self.filename, 'w+')
            # indent=2生成更可读的json
            return json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.debug('保存', self.filename, '失败！', e)
            return False
        except:
            raise


    def check(self, proxy):
        """
        检测代理是否有效
        :param proxy:
        :return:
        """
        if not proxy:
            self.logger.debug(u'检测到无效代理%s!' % proxy)
            return None
        proxy_handler = urllib2.ProxyHandler({'http': proxy})
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1')]
        urllib2.install_opener(opener)

        try:
            # 记录开始时间
            start = time.time()
            self.logger.debug(u'开始检测%s连接情况' % proxy)
            html = urllib2.urlopen(url=self.test_url, timeout=self.timeout).read()
            used = time.time() - start
            # 如果返回的内容正常，并且没有超时
            if html.find(u'百度') > 1 and used <= self.timeout:
                self.logger.debug(u'代理正常：%s 连接时间：%s' % ( proxy, used ))
                return proxy
            else:
                self.logger.debug(u'%s连接超时' % proxy)
                return None
        except Exception as e:
            self.logger.debug(u'检测代理 %s 出错，原因：%s ' % (proxy, e))
        except:
            self.logger.debug(u'proxy.check出现未知错误！')
            raise


proxy = Proxy()
def load(type='http', refresh=False):
    return proxy.load(type,refresh)

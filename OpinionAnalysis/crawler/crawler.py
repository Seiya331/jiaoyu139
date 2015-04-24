#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
爬虫基类，实现基本的自动代理、超时重试请求数据
"""

import sys
import re
reload(sys)
sys.setdefaultencoding('utf8')
import urllib2
from random import choice
from . import proxy
from . import logger


class Crawler(object):
    def __init__(self, headers=None):
        """
        初始化
        :param headers:
        :return:
        """
        if headers is None:
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
            }
        else:
            self.headers = headers
        # 加载代理列表
        self.proxies = proxy.load(type='http')

        #默认的超时时间为10秒
        self.timeout = 10

        self.logger = logger.get('opinion.crawler.Crawler')

    def textFilter(self,content,force=True):
        html = re.compile(r'<.*?>|&.*?;|@?|//@.*|\[[^]]+\]|回复.*:')
        content = html.sub('',content)
        #必须屏蔽美丽说这个词！影响结果
        if force:
            return content.replace(u'美丽说','')
        else:
            return content

    def request(self, url, data=None, useProxy=False, retry=3, headers=None):
        """
        抓取指定URL的数据
        :param url: URL地址
        :param data: POST的数据
        :param useProxy: 是否使用代理，默认不使用
        :param retry:   重试次数
        :return:
        """

        if headers is not None:
            self.headers = headers

        # 如果要求使用代理
        if useProxy is True and self.proxies:
            # 随机选择一个代理
            http = choice(self.proxies)
            self.logger.debug(u'设置代理  %s ' % http)
            proxy_handler = urllib2.ProxyHandler({"http": http})
        else:
            self.logger.debug(u'未使用代理！')
            proxy_handler = urllib2.ProxyHandler({})

        encoding_support = ContentEncodingProcessor
        # 设置代理
        opener = urllib2.build_opener(encoding_support, proxy_handler, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

        #构造请求对象
        request = urllib2.Request(
            url=url,
            data=data,
            headers=self.headers
        )
        try:
            #请求数据
            self.logger.debug(u'开始抓取  %s ' % url)
            response = urllib2.urlopen(request, timeout=10).read()

            self.logger.debug(u'抓取 %s 结束.' % url)
            return response

        #处理各种异常情况
        except Exception as e:
            #超时的话自动重试
            self.logger.debug(u'抓取 %s 失败，原因：%s 重试次数 %s ' % (url, e, retry))
            if retry > 0:
                return self.request(url, data, useProxy, retry - 1)
            self.logger.error(u'超过尝试次数，%s抓取失败 %s' % (url,e))
            return None
        except:
            self.logger.error(u'crawler.request 出现未知错误！')
            raise

    def request_response(self, url, data=None, useProxy=False, retry=3, headers=None):
        """
        抓取指定URL的数据
        :param url: URL地址
        :param data: POST的数据
        :param useProxy: 是否使用代理，默认不使用
        :param retry:   重试次数
        :return:
        """

        if headers is not None:
            self.headers = headers

        # 如果要求使用代理
        if useProxy is True and self.proxies:
            # 随机选择一个代理
            http = choice(self.proxies)
            self.logger.debug(u'设置代理  %s ' % http)
            proxy_handler = urllib2.ProxyHandler({"http": http})
        else:
            self.logger.debug(u'未使用代理！')
            proxy_handler = urllib2.ProxyHandler({})

        encoding_support = ContentEncodingProcessor
        # 设置代理
        opener = urllib2.build_opener(encoding_support, proxy_handler, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

        #构造请求对象
        request = urllib2.Request(
            url=url,
            data=data,
            headers=self.headers
        )
        try:
            #请求数据
            self.logger.debug(u'开始抓跳转url  %s ' % url)
            response = urllib2.urlopen(request, timeout=10)
            if response is None:
                self.logger.debug(u'跳转url抓取失败')
            else:
                return response.geturl()
            self.logger.debug(u'开始抓跳转url %s 结束.' % url)

        #处理各种异常情况
        except Exception as e:
            #超时的话自动重试
            self.logger.debug(u'开始抓跳转url %s 失败，原因：%s 重试次数 %s ' % (url, e, retry))
            if retry > 0:
                return self.request_response(url, data, useProxy, retry - 1)
            self.logger.error(u'开始抓跳转url超过尝试次数，%s抓取失败 %s' % (url,e))
            return None
        except:
            self.logger.error(u'crawler.request 抓跳转url出现未知错误！')
            raise


from gzip import GzipFile
from StringIO import StringIO
import zlib


class ContentEncodingProcessor(urllib2.BaseHandler):
    """
    来源：http://www.pythonclub.org/python-network-application/observer-spider
    A handler to add gzip capabilities to urllib2 requests
    """

    def __init__(self):
        pass

    # add headers to requests
    def http_request(self, req):
        req.add_header("Accept-Encoding", "gzip, deflate")
        return req

    # decode
    def http_response(self, req, resp):
        old_resp = resp

        # gzip
        if resp.headers.get("content-encoding") == "gzip":
            if resp.headers.get("transfer-encoding") == "chunked":
                d = zlib.decompressobj(16+zlib.MAX_WBITS) #this magic number can be inferred from the structure of a gzip file
                data = resp.read()
                data = d.decompress(data)
                resp = urllib2.addinfourl(StringIO(data), old_resp.headers, old_resp.url,old_resp.code)
                resp.msg = old_resp.msg
            else:
                gz = GzipFile(
                    fileobj=StringIO(resp.read()),
                    mode="r"
                )
                resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url,old_resp.code)
                resp.msg = old_resp.msg

        # deflate
        if resp.headers.get("content-encoding") == "deflate":
            gz = StringIO(deflate(resp.read()))
            resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)  # 'class to add info() and
            resp.msg = old_resp.msg
        return resp

# deflate support

def deflate(data):  # zlib only provides the zlib compress format, not the deflate format;
    try:  # so on top of all there's this workaround:
        return zlib.decompress(data, -zlib.MAX_WBITS)
    except zlib.error:
        return zlib.decompress(data)



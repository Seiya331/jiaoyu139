#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
import time
import urllib
from .crawler import Crawler
from . import logger
from . import c_tool
#解析xml
from xml.etree import ElementTree
import sys

class BaiduNewsCrawler(Crawler):

    def __init__(self,keyword):
        """
        百度新闻爬虫
        :param keyword:
        :return:
        """
        Crawler.__init__(self)
        if not keyword:
            raise RuntimeError('请提供搜索关键词')
        self.keyword = keyword

        self.refer = 'http://m.baidu.com/news?fr=mohome'
        self.api = u'http://m.baidu.com/news?tn=bdapisearch&word=%s&pn=%s&rn=%s'
        #起始数据数据
        self.pn = 0
        #row number每行新闻的数量
        self.rn = 20
        self.logger = logger.get('opinion.crawler.BaiduNewsCrawler')
        self.headers = {
            'Accept':'application/json',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
            'X-Requested-With':'XMLHttpRequest',
        }

    def read(self,pn=None,rn=None):
        """
        读取微博内容
        :param page: 页码
        :param count: 每页的微博数量
        :return:
        """
        #如果手动设置了要抓取的页面
        if pn is not None:
            self.pn = pn > 0 and pn or 0
        if rn is not None:
            self.count = rn > 0 and rn or 20


        url = self.api % (self.keyword,self.pn,self.rn)

        #请求数据
        result = self.request(url,useProxy=True,headers=self.headers)
        #如果请求失败
        if result is None:
            self.logger.debug('抓取%s数据失败！' % url)
            return []
        try:
            info = json.loads(result)
        except Exception,e:
            self.logger.error('格式化 百度新闻 JSON数据出错 %s ' % e )
            return []
        #如果数据不正确
        if not info:
            self.logger.debug('%s 返回数据为空' % url)
            return []

        #自动进入下一页数据
        self.pn += self.rn
        #对微博的消息内容进行分析
        #return analysis(info,type='baidu_news')
        return self.format(info)

    def format(self,n_list):
        """
         {
    "title": "天津金融资产交易所携手淘宝搭建“中国资产拍卖会”",
    "url": "http://news.china.com/zh_cn/finance/11155042/20141119/18983604.html",
    "author": "中华网",
    "abs": ")19日,由天津金融资产交易所与淘宝网共同搭建的��中国资产拍卖会��正式上线。",
    "sortTime": "1416380874",
    "publicTime": "1416380874",
    "imgUrl": ""
}
        """
        new_list = []
        try:
            for m in n_list:
                if str(m.get('title','') + m.get('abs','')).find('美丽说') == -1:
                    continue
                fmt = {}
                fmt['unique_identify'] =  m['url']
                fmt['title'] = m['title']
                fmt['summary'] =  m['abs']
                fmt['text_content'] = self.textFilter(m.get('title','') + m.get('abs',''))
                fmt['source'] = '百度新闻'
                fmt['type'] = 2 #新闻
                fmt['author'] = m['author']
                fmt['link'] = m['url']
                fmt['pub_date'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(m['publicTime'])))
                #额外记录该微博用户的信息
                fmt['json_data'] = {
                    'img_url':m['imgUrl'],
                }
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化 百度新闻 出错 %s ' % e )
        return new_list



class So360NewsCrawler(Crawler):
    """
    360新闻爬虫
    """
    def __init__(self,keyword):
        """
        :param keyword:
        :return:
        """
        Crawler.__init__(self)
        if not keyword:
            raise RuntimeError('请提供搜索关键词')
        self.keyword = keyword
        self.api = u'http://m.news.so.com/ns?q=%s&pn=%s&fmt=html'
        #起始数据数据
        self.pn = 1
        #row number每行新闻的数量
        self.rn = 0
        self.logger = logger.get('opinion.crawler.So360NewsCrawler')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
            'X-Requested-With':'XMLHttpRequest',
        }
        self.extract_pattern = ur'data-index="\d?">.*?href="(.*?)">.*?class=title>(.*?)</span>.*?class=detail>.*?class=content>.*?class=summary>(.*?)</p>.*?class="info-source">(.*?)</span>.*?class="info-publush-date">(.*?)</time>'

    def read(self,pn=None,rn=None):
        """
        读取微博内容
        :param page: 页码
        :param count: 每页的微博数量
        :return:
        """
        #如果手动设置了要抓取的页面
        if pn is not None:
            self.pn = pn > 0 and pn or 0
        if rn is not None:
            self.count = rn > 0 and rn or 20

        if self.pn == 1 :
            self.headers['Referer'] = self.api % (self.keyword, 1)
        else:
            self.headers['Referer'] = self.api % (self.keyword, self.pn-1)

        url = self.api % (self.keyword,self.pn)

        #请求数据
        html = self.request(url,useProxy=True,headers=self.headers)
        #如果请求失败
        if html is None:
            self.logger.debug('抓取%s数据失败！' % url)
            return []

        regex = re.compile(self.extract_pattern)

        info = []
        regex_match_all = re.findall(regex, html)
        if regex_match_all is None:
            self.logger.debug('%s,抓取%s数据失败！' % (self.keyword,url))
            return []
        for match in regex_match_all:
            info.append({
                'url': match[0],
                'title':match[1],
                'summary':match[2],
                'source':match[3],
                'pub_date':match[4],
            })

        #如果数据不正确
        if not info:
            self.logger.debug('%s 返回数据为空' % url)
            return []

        #自动进入下一页数据
        self.pn += 1
        #对微博的消息内容进行分析
        #return analysis(info,type='news_so360')
        return self.format(info)


    def format(self,n_list):
        """
        内容是使用正则提取的HTML，所以没有具体JSON格式
        :param n_list:
        :return:
        """
        new_list = []
        p = re.compile(ur'&amp;u=(.*)\s*')
        try:
            for m in n_list:
                if str(m['title'] + m['summary']).find('美丽说') == -1:
                    continue
                fmt = {}
                u = re.search(p, urllib.unquote(m['url']))
                if u :
                    fmt['link'] = u.group(1)
                else:
                    fmt['link'] = m['url']
                #取链接作为唯一标识
                fmt['unique_identify'] = fmt['link']
                fmt['title'] = m['title']
                fmt['summary'] =  m['summary']
                fmt['text_content'] = self.textFilter(m['title'] + m['summary'])
                fmt['source'] = '360新闻'
                fmt['type'] = 2 #新闻
                fmt['author'] = m['source']
                fmt['pub_date'] = m['pub_date']
                #额外记录该微博用户的信息
                fmt['json_data'] = {}
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化 360新闻 出错 %s ' % e )
        return new_list


class SogouWenCrawler(Crawler):

    def __init__(self,keyword):
        """
        百度新闻爬虫
        :param keyword:
        :return:
        """
        Crawler.__init__(self)
        if not keyword:
            raise RuntimeError('请提供搜索关键词')
        self.keyword = keyword
        self.api = u'http://wenwen.m.sogou.com/api/action.jsp?ac=31&key=%s&pn=%s&ps=%s&state=104'
        #起始数据数据
        self.pn = 1
        #row number每行新闻的数量
        self.rn = 10
        self.logger = logger.get('opinion.crawler.SogouWenCrawler')
        self.headers = {
            'Accept':'application/json',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
            'X-Requested-With':'XMLHttpRequest',
        }

    def read(self,pn=None,rn=None):
        """
        读取微博内容
        :param page: 页码
        :param count: 每页的微博数量
        :return:
        """
        #如果手动设置了要抓取的页面
        if pn is not None:
            self.pn = pn > 0 and pn or 0
        if rn is not None:
            self.count = rn > 0 and rn or 20


        url = self.api % (self.keyword,self.pn,self.rn)

        #请求数据
        result = self.request(url,useProxy=True,headers=self.headers)
        #如果请求失败
        if result is None:
            self.logger.debug('抓取%s数据失败！' % url)
            return []
        try:
            info = json.loads(result)
        except Exception,e:
            self.logger.error('格式化 搜狗问问 出错 %s ' % e )
            return []
        #如果数据不正确
        if not info:
            self.logger.debug('%s 返回数据为空' % url)
            return []

        #自动进入下一页数据
        self.pn += 1
        #对微博的消息内容进行分析
        #return analysis(info,type='baidu_news')
        return self.format(info)

    def format(self,n_list):
        """
       {
            "content": "恩恩",
            "id": 624930924,
            "time": "03月21日",
            "title": "美丽说</em>真是个垃圾</em>网站。10天不发货还特么联系。第",
            "answerNum": 1,
            "state": 1,
            "clk": "1944575517_-973475323_1428902467381629471_865484,500,1,1,104",
            "ansZanTotal": 0
        },
        }
        """
        new_list = []
        try:
            for m in n_list['quList']:
                if str(m.get('title','') + m.get('content','')).find('美丽说') == -1:
                    continue
                fmt = {}
                fmt['unique_identify'] = "http://wenwen.sogou.com/z/q%s.htm" %m['id']
                fmt['title'] = m['title']
                fmt['summary'] =  m['title']
                fmt['text_content'] = self.textFilter(m.get('title','') + m.get('content',''))
                fmt['source'] = '搜狗问问'
                fmt['type'] = 2 #新闻
                fmt['author'] = ''
                fmt['link'] =  "http://wenwen.sogou.com/z/q%s.htm" %m['id']
                fmt['pub_date'] = self.format_time(m['time'])
                #额外记录该用户的信息
                fmt['json_data'] = {
                    'answerNum':m['answerNum'],
                }
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化 搜狗问问 出错 %s ' % e )
        return new_list

    #格式化时间
    def format_time(self,data):
        try:
            regex = re.compile(ur'\d+')
            match = re.findall(regex, data)
            if int(match[0]) >1000:
                return  match[0]+'-'+ match[1]+'-01 00:00:00'
            else :
                return  time.strftime('%Y',time.localtime(time.time()))+'-'+match[0]+'-'+ match[1]+' 00:00:00'
        except Exception:
            return  time.strftime('%Y-%m-%d H:i:s',time.localtime(time.time()))

#人民网
class PeopleNewsCrawler(Crawler):
    """
    人民网
    """
    def __init__(self,keyword):
        """
        :param keyword:
        :return:
        """
        Crawler.__init__(self)
        if not keyword:
            raise RuntimeError('请提供搜索关键词')
        self.keyword = keyword
        self.api = u'http://search.people.com.cn/rmw/GB/rmwsearch/gj_searchht.jsp'
        #起始数据数据
        self.pn = 1
        #row number每行新闻的数量
        self.rn = 0
        self.logger = logger.get('opinion.crawler.PeopleNewsCrawler')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:37.0) Gecko/20100101 Firefox/37.0',
            'X-Requested-With':'XMLHttpRequest',
            #'Content-Type':'application/x-www-form-urlencoded'
        }

    def read(self,pn=None,rn=None):
        """
        读取微博内容
        :param page: 页码
        :param count: 每页的微博数量
        :return:
        """
        #如果手动设置了要抓取的页面
        if pn is not None:
            self.pn = pn > 0 and pn or 0
        if rn is not None:
            self.count = rn > 0 and rn or 20
        data={'basenames':'rmwsite',
              'classfield':'CLASS2',
              'classvalue':'ALL',
              'curpage':self.pn,
              'isclass':1,
              'keyword':self.keyword,
              'pagecount':20,
              'sortfield':'-INPUTTIME',
              'where':'(TITLE=(%s) or AUTHOR=(%s))' %(self.keyword,self.keyword)
        }
        #data 数据编码
        url = self.api
        #请求数据
        data=urllib.urlencode(data)
        html = self.request(url,data,useProxy=True,headers=self.headers)
        #如果请求失败
        if html is None:
            self.logger.debug('抓取%s数据失败！' % url)
            return []
        try:
            info = self.parse_xml(html)
        except Exception,e:
            self.logger.debug('%s xml 数据解析错误 ，错误原因' %(url,e))
            info =[]
        #如果数据不正确
        if not info:
            self.logger.debug('%s 返回数据为空' % url)
            return []

        #自动进入下一页数据
        self.pn += 1
        #对微博的消息内容进行分析
        #return analysis(info,type='news_so360')
        return self.format(info)


    def format(self,n_list):
        """
        内容是使用正则提取的HTML，所以没有具体JSON格式
        :param n_list:
        :return:
        """
        new_list = []
        #p = re.compile(ur'&amp;u=(.*)\s*')
        try:
            for m in n_list:
                if str(m['title'] + m['summary']).find('美丽说') == -1:
                    continue
                fmt = {}
                fmt['link'] = m['url']
                #取链接作为唯一标识
                fmt['unique_identify'] = fmt['link']
                fmt['title'] = m['title']
                fmt['summary'] =  m['summary']
                fmt['text_content'] = self.textFilter(m['title'] + m['summary'])
                fmt['source'] = '人民网'
                fmt['type'] = 2 #新闻
                fmt['author'] = m['source']
                fmt['pub_date'] = m['pub_date']
                #额外记录该微博用户的信息
                fmt['json_data'] = {}
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化 人民网资讯 出错 %s ' % e )
        return new_list
    #解析xml
    def parse_xml(self,xml):
        root = ElementTree.fromstring(xml)
        # 获取element的方法
        # 1 通过getiterator
        lst_node = root.getiterator("RESULT")
        info = []
        for node in lst_node:
            node_find = node.find('TITLE')
            title = node_find.text
            node_find = node.find('CONTENT')
            content = node_find.text
            node_find = node.find('AUTHOR')
            author = node_find.text
            if author == None  :
                author = '人民网'
            node_find = node.find('PUBLISHTIME')
            pub_date = node_find.text
            node_find = node.find('DOCURL')
            url = node_find.text
            regex = re.compile(ur'\d+')
            match = re.findall(regex, pub_date)
            pub_date = '%s-%s-%s %s:%s:%s' %(match[0],match[1],match[2],match[3],match[4],match[4])
            info.append({
                'url': url,
                'title':title.decode('utf-8'),
                'summary':content.decode('utf-8'),
                'source': author ,
                'pub_date':pub_date,
            })
        return info

class EC100NewsCrawler(Crawler):
    """
    中国电子商务网
    """
    def __init__(self,keyword):
        """
        :param keyword:
        :return:
        """
        Crawler.__init__(self)
        if not keyword:
            raise RuntimeError('请提供搜索关键词')
        self.keyword = keyword
        self.api = 'http://www.100ec.cn/search.cgi?p=%s&f=search&%s'
        self.api_url = u'http://www.100ec.cn'
        #起始数据数据
        self.pn = 1
        #row number每行新闻的数量
        self.rn = 0
        self.logger = logger.get('opinion.crawler.EC100NewsCrawler')
        self.headers = {
             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:37.0) Gecko/20100101 Firefox/37.0',
             'Content-Type':'application/x-www-form-urlencoded;charset=gb2312'
        }
        self.extract_pattern = ur'<li>.*?href="(.*?)" target=_blank>(.*?)<\/a>.*?class="f_hui">\((.*?)-(.*?)\)<\/span><\/li>'

    def read(self,pn=None,rn=None):
        """
        读取微博内容
        :param page: 页码
        :param count: 每页的微博数量
        :return:
        """
        #如果手动设置了要抓取的页面
        if pn is not None:
            self.pn = pn > 0 and pn or 0
        if rn is not None:
            self.count = rn > 0 and rn or 20

        terms =urllib.urlencode({'terms':self.keyword.encode('GB2312')})
        if self.pn == 1 :
            self.headers['Referer'] = self.api % (1,terms)
        else:
            self.headers['Referer'] = self.api % (self.pn,terms)

        url = self.api % (self.pn,terms)
        #请求数据
        html = self.request(url,useProxy=True,headers=self.headers)
        #如果请求失败
        if html is None:
            self.logger.debug('抓取%s数据失败！' % url)
            return []

        regex = re.compile(self.extract_pattern)
        info = []
        regex_match_all = re.findall(regex, html)
        if regex_match_all is None:
            self.logger.debug('%s,抓取%s数据失败！' % (self.keyword,url))
            return []
        current_year = time.strftime('%Y',time.localtime(time.time()))
        now_month = time.strftime('%m',time.localtime(time.time()))
        for match in regex_match_all:
            if len(match) <4:
                continue
            try:
                if match[2] <= now_month:
                    pub_date = '%s-%s-%s 00:00:00' %(str(current_year),str(match[2]),
                                                     str(match[3]))
                else:
                    pub_date = '%s-%s-%s 00:00:00' %(str(int(current_year)-1),str(match[2]),
                                                     str(match[3]))
                title = c_tool.tool_strip_tag(match[1].decode('gb2312'))
                info.append({
                    'url': self.api_url+match[0].decode('gb2312'),
                    'title':title,
                    'summary':title,
                    'source':'中国电子商务网',
                    'pub_date':pub_date,
                })
            except Exception,e:
                 self.logger.debug('正则匹配数据错误 %s 错误原因 %s' % (url,e))
        #如果数据不正确
        if not info:
            self.logger.debug('%s 返回数据为空' % url)
            return []

        #自动进入下一页数据
        self.pn += 1
        #对微博的消息内容进行分析
        #return analysis(info,type='news_so360')
        return self.format(info)


    def format(self,n_list):
        """
        内容是使用正则提取的HTML，所以没有具体JSON格式
        :param n_list:
        :return:
        """
        new_list = []
        try:
            for m in n_list:
                if str(m['title'] + m['summary']).find('美丽说') == -1:
                    continue
                fmt = {}

                fmt['link'] = m['url']
                #取链接作为唯一标识
                fmt['unique_identify'] = fmt['link']
                fmt['title'] = m['title']
                fmt['summary'] =  m['summary']
                fmt['text_content'] = self.textFilter(m['title'] + m['summary'])
                fmt['source'] = '中国电子商务网'
                fmt['type'] = 2 #新闻
                fmt['author'] = m['source']
                fmt['pub_date'] = m['pub_date']
                #额外记录该微博用户的信息
                fmt['json_data'] = {}
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化 EC100 出错 %s ' % e )
        return new_list

class NenNewsCrawler(Crawler):
    """
    NEN财经
    """
    def __init__(self,keyword):
        """
        :param keyword:
        :return:
        """
        Crawler.__init__(self)
        if not keyword:
            raise RuntimeError('请提供搜索关键词')
        self.keyword = keyword
        self.api = 'http://so.nen.com.cn/m_fullsearch/full_search.jsp'
        #self.api_url = u'http://www.100ec.cn'
        #起始数据数据
        self.pn = 1
        #row number每行新闻的数量
        self.rn = 20
        self.logger = logger.get('opinion.crawler.NenNewsCrawler')
        self.headers = {
             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:37.0) Gecko/20100101 Firefox/37.0',
             'Content-Type':'application/x-www-form-urlencoded;charset=gb2312'
        }
        self.extract_pattern = r'<tr>.*?href="(.*?)">(.*?)<\/a>.*?target=\'_blank\'>(.*?)<\/a>.*?class="searchMain">(.*?)<\/td>.*?&nbsp(\d{1,4}-\d{1,4}-\d{1,4})<br><br><\/td>'

    def read(self,pn=None,rn=None):
        """
        读取微博内容
        :param page: 页码
        :param count: 每页的微博数量
        :return:
        """
        #如果手动设置了要抓取的页面
        if pn is not None:
            self.pn = pn > 0 and pn or 0
        if rn is not None:
            self.count = rn > 0 and rn or 20

        data={'channel_id':0,
              'keywords':self.keyword.encode('GB2312'),
              'pagen':self.pn,
              'size':self.rn,
              'sort':2,
              'title':self.keyword.encode('GB2312')
        }
        #请求数据
        data=urllib.urlencode(data)
        url = self.api
        #请求数据
        html = self.request(url,data,useProxy=True,headers=self.headers)
        #如果请求失败
        if html is None:
            self.logger.debug('抓取%s数据失败！' % url)
            return []
        html = c_tool.tool_trim(html)
        regex = re.compile(self.extract_pattern)
        info = []
        regex_match_all = re.findall(regex, html)
        if regex_match_all is None:
            self.logger.debug('%s,抓取%s数据失败！' % (self.keyword,url))
            return []
        for match in regex_match_all:
            if len(match) <5:
                continue
            try:
                title = match[1].decode('gb2312').encode('utf-8')
                info.append({
                    'url': match[0],
                    'title':c_tool.tool_strip_tag(match[1].decode('gb2312').encode('utf-8')),
                    'summary':c_tool.tool_strip_tag(match[3].decode('gb2312').encode('utf-8')),
                    'source':match[2].decode('gb2312').encode('utf-8'),
                    'pub_date':match[4]
                })
            except Exception,e:
                 self.logger.debug('正则匹配数据错误 %s 错误原因 %s' % (url,e))
        #如果数据不正确
        if not info:
            self.logger.debug('%s 返回数据为空' % url)
            return []

        #自动进入下一页数据
        self.pn += 1
        #对微博的消息内容进行分析
        #return analysis(info,type='news_so360')
        return self.format(info)


    def format(self,n_list):
        """
        内容是使用正则提取的HTML，所以没有具体JSON格式
        :param n_list:
        :return:
        """
        new_list = []
        try:
            for m in n_list:
                if str(m['title'] + m['summary']).find('美丽说') == -1:
                    continue
                fmt = {}
                fmt['link'] = m['url']
                #取链接作为唯一标识
                fmt['unique_identify'] = fmt['link']
                fmt['title'] = m['title']
                fmt['summary'] =  m['summary']
                fmt['text_content'] = self.textFilter(m['title'] + m['summary'])
                fmt['source'] = 'NEN财经'
                fmt['type'] = 2 #新闻
                fmt['author'] = m['source']
                fmt['pub_date'] = m['pub_date']
                #额外记录该微博用户的信息
                fmt['json_data'] = {}
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化 NEN财经 出错 %s ' % e )
        return new_list

class YcNewsCrawler(Crawler):
    """
    宜春新闻网
    http://bbs.newsyc.com:9080/servlet/SearchServlet.do?contentKey=美丽说&titleKey
    =&authorKey=&nodeNameResult=&subNodeResult=&dateFrom=&dateEnd=&sort=date&op=single&siteID=&pager.offset=10&pageNo=1
    """
    def __init__(self,keyword):
        """
        :param keyword:
        :return:
        """
        Crawler.__init__(self)
        if not keyword:
            raise RuntimeError('请提供搜索关键词')
        self.keyword = keyword
        self.api = 'http://bbs.newsyc.com:9080/servlet/SearchServlet.do?contentKey' \
                   '=%s&titleKey=&authorKey=&nodeNameResult=&subNodeResult=&dateFrom' \
                   '=&dateEnd=&sort=date&op=single&siteID=&pager.offset=%s&pageNo=%s'
        #self.api_url = u'http://www.100ec.cn'
        #起始数据数据
        self.pn = 1
        #row number每行新闻的数量
        self.rn = 20
        self.logger = logger.get('opinion.crawler.NenNewsCrawler')
        self.headers = {
             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:37.0) Gecko/20100101 Firefox/37.0',
             'Content-Type':'application/x-www-form-urlencoded;charset=utf-8'
        }
        self.extract_pattern = ur'<tr.*?href="(.*?)" target="_blank">(.*?)<\/a>.*?<br>(.*?)<br>'

    def read(self,pn=None,rn=None):
        """
        读取微博内容
        :param page: 页码
        :param count: 每页的微博数量
        :return:
        """
        #如果手动设置了要抓取的页面
        if pn is not None:
            self.pn = pn > 0 and pn or 0
        if rn is not None:
            self.rn = rn > 0 and rn or 20

        self.headers['Referer'] = self.api % (self.keyword,self.rn,self.pn)

        url = self.api % (self.keyword,self.rn,self.pn)

        html = self.request(url,useProxy=True,headers=self.headers)

        #如果请求失败
        if html is None:
            self.logger.debug('抓取%s数据失败！' % url)
            return []
        #去除空格
        html = c_tool.tool_trim(html)
        regex = re.compile(self.extract_pattern)
        info = []
        time_regex = re.compile(ur'(\d{4})-(\d{1,2})\/(\d{1,2})')
        regex_match_all = re.findall(regex, html)
        if regex_match_all is None:
            self.logger.debug('%s,抓取%s数据失败！' % (self.keyword,url))
            return []
        for match in regex_match_all:
            if len(match) <3:
                continue
            try:
                time_info = re.findall(time_regex,match[0])
                time_tuple = time_info[0]
                info.append({
                    'url': match[0],
                    'title':c_tool.tool_strip_tag(match[1]),
                    'summary':c_tool.tool_strip_tag(match[2]),
                    'source':'宜春新闻网',
                    'pub_date':'%s-%s-%s' %(time_tuple[0],time_tuple[1],time_tuple[2])
                })
            except Exception,e:
                 self.logger.debug('正则匹配数据错误 %s 错误原因 %s' % (url,e))
        #如果数据不正确
        if not info:
            self.logger.debug('%s 返回数据为空' % url)
            return []
        #自动进入下一页数据
        self.pn += 1
        #对微博的消息内容进行分析
        #return analysis(info,type='news_so360')
        return self.format(info)


    def format(self,n_list):
        """
        内容是使用正则提取的HTML，所以没有具体JSON格式
        :param n_list:
        :return:
        """
        new_list = []
        try:
            for m in n_list:
                if str(m['title'] + m['summary']).find('美丽说') == -1:
                    continue
                fmt = {}
                fmt['link'] = m['url']
                #取链接作为唯一标识
                fmt['unique_identify'] = fmt['link']
                fmt['title'] = m['title']
                fmt['summary'] =  m['summary']
                fmt['text_content'] = self.textFilter(m['title'] + m['summary'])
                fmt['source'] = '宜春新闻网'
                fmt['type'] = 2 #新闻
                fmt['author'] = m['source']
                fmt['pub_date'] = m['pub_date']
                #额外记录该微博用户的信息
                fmt['json_data'] = {}
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化 宜春新闻网 出错 %s ' % e )
        return new_list


class IKanChaiCrawler(Crawler):
    """
     科技快报 http://so.ikanchai.com/cse/search?%s&s=754371921301160334&nsid=2
    """
    def __init__(self,keyword):
        """
        :param keyword:
        :return:
        """
        Crawler.__init__(self)
        if not keyword:
            raise RuntimeError('请提供搜索关键词')
        self.keyword = keyword
        self.api = u'http://so.ikanchai.com/cse/search?%s&s=754371921301160334&nsid=2'
        #起始数据数据
        self.pn = 0
        #row number每行新闻的数量
        self.rn = 0
        self.logger = logger.get('opinion.crawler.IKanChaiCrawler')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:37.0) Gecko/20100101 Firefox/37.0',
        }
        self.extract_pattern = r'<div class="result.*?href="(.*?)".*?>(.*?)<\/a>.*?class="c-abstract"\s>(.*?)class="c-showurl".*?(\d{1,4}-\d{1,4}-\d{1,4})<\/span>'
    def read(self,pn=None,rn=None):
        """
        读取微博内容
        :param page: 页码
        :param count: 每页的微博数量
        :return:
        """
        #如果手动设置了要抓取的页面
        if pn is not None:
            self.pn = pn > 0 and pn or 0
        data = {
            'q':self.keyword,
            'p':self.pn
        }
        params = urllib.urlencode(data)
        self.headers['Referer'] = self.api % (params)
        url = self.api % (params)

        #请求数据
        html = self.request(url,useProxy=True,headers=self.headers)
        #如果请求失败
        if html is None:
            self.logger.debug('抓取%s数据失败！' % url)
            return []
        html = c_tool.tool_trim(html)
        regex = re.compile(self.extract_pattern)
        info =[]
        regex_match_all = re.findall(regex, html)
        if regex_match_all is None:
            self.logger.debug('%s,抓取%s数据失败！' % (self.keyword,url))
            return []
        for match in regex_match_all:
            if len(match) <4:
                continue
            try:
                info.append({
                    'url': match[0],
                    'title':c_tool.tool_strip_tag(match[1]),
                    'summary':c_tool.tool_strip_tag(match[2]),
                    'source':'科技快报',
                    'pub_date':match[3],

                })
            except Exception,e:
                 self.logger.debug('正则匹配数据错误 %s 错误原因 %s' % (url,e))
        #如果数据不正确
        if not info:
            self.logger.debug('%s 返回数据为空' % url)
            return []
        #自动进入下一页数据
        self.pn += 1
        #对微博的消息内容进行分析
        #return analysis(info,type='news_so360')
        return self.format(info)
    def format(self,n_list):
        """
        内容是使用正则提取的HTML，所以没有具体JSON格式
        :param n_list:
        :return:
        """
        new_list = []
        try:
            for m in n_list:
                if str(m['title']).find('美丽说') == -1:
                    continue
                fmt = {}
                fmt['link'] = m['url']
                #取链接作为唯一标识
                fmt['unique_identify'] = fmt['link']
                fmt['title'] = m['title']
                fmt['summary'] =  m['summary']
                fmt['text_content'] = self.textFilter(m['title'] + m['summary'])
                fmt['source'] = '科技快报'
                fmt['type'] = 2 #新闻
                fmt['author'] = m['source']
                fmt['pub_date'] = m['pub_date']
                #额外记录该微博用户的信息
                fmt['json_data'] = {}
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化  科技快报 出错 %s ' % e )
        return new_list




class HeXunNewsCrawler(Crawler):
    """
     和讯网 http://so.ikanchai.com/cse/search?%s&s=754371921301160334&nsid=2
    """
    def __init__(self,keyword):
        """
        :param keyword:
        :return:
        """
        Crawler.__init__(self)
        if not keyword:
            raise RuntimeError('请提供搜索关键词')
        self.keyword = keyword
        self.api = u'http://news.search.hexun.com/news?%s&s=1&t=0&f=1'
        #起始数据数据
        self.pn = 1
        #row number每行新闻的数量
        self.rn = 0
        self.logger = logger.get('opinion.crawler.HeXunNewsCrawler')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:37.0) Gecko/20100101 Firefox/37.0',
        }
        self.extract_pattern = r'<div.*?class="newslist-a.*?href="(.*?)" target="_blank">(.*?)<\/div>.*?class="news-l-c">(.*?)<\/div>'
    def read(self,pn=None,rn=None):
        """
        读取微博内容
        :param page: 页码
        :param count: 每页的微博数量
        :return:
        """
        #如果手动设置了要抓取的页面
        if pn is not None:
            self.pn = pn > 0 and pn or 0
        data = {
            'key':self.keyword.encode('gb2312'),
            'page':self.pn,
        }
        params = urllib.urlencode(data)
        self.headers['Referer'] = self.api % (params)
        url = self.api % (params)
        #请求数据
        html = self.request(url,useProxy=True,headers=self.headers)
        #如果请求失败
        if html is None:
            self.logger.debug('抓取%s数据失败！' % url)
            return []
        html = c_tool.tool_trim(html)
        regex = re.compile(self.extract_pattern)
        info =[]
        regex_match_all = re.findall(regex, html)
        if regex_match_all is None:
            self.logger.debug('%s,抓取%s数据失败！' % (self.keyword,url))
            return []
        for match in regex_match_all:
            if len(match) <3:
                continue
            try:
                info.append({
                    'url': match[0].decode('gb2312').encode('utf-8'),
                    'title':c_tool.tool_strip_tag(match[1].decode('gb2312').encode('utf-8')),
                    'summary':c_tool.tool_strip_tag(match[2].decode('gb2312').encode('utf-8')),
                    'source':'和讯',
                    'pub_date':self.analysis_time(match[0]),

                })
            except Exception,e:
                 self.logger.debug('正则匹配数据错误 %s 错误原因 %s' % (url,e))

        #如果数据不正确
        if not info:
            self.logger.debug('%s 返回数据为空' % url)
            return []
        #自动进入下一页数据
        self.pn += 1
        #对微博的消息内容进行分析
        #return analysis(info,type='news_so360')
        return self.format(info)
    def format(self,n_list):
        """
        内容是使用正则提取的HTML，所以没有具体JSON格式
        :param n_list:
        :return:
        """
        new_list = []
        try:
            for m in n_list:
                if str(m['title'] + m['summary']).find('美丽说') == -1:
                    continue
                fmt = {}
                fmt['link'] = m['url']
                #取链接作为唯一标识
                fmt['unique_identify'] = fmt['link']
                fmt['title'] = m['title']
                fmt['summary'] =  m['summary']
                fmt['text_content'] = self.textFilter(m['title'] + m['summary'])
                fmt['source'] = '和讯网'
                fmt['type'] = 2 #论坛
                fmt['author'] = m['source']
                fmt['pub_date'] = m['pub_date']
                #额外记录该微博用户的信息
                fmt['json_data'] = {}
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化  和讯网 出错 %s ' % e )
        return new_list

    #解析时间返回需要的时间
    def analysis_time(self,data):
        #02月28日 17:22
        content_regex = re.compile(r'(\d{1,4}-\d{1,2}-\d{1,2})')
        match = re.findall(content_regex, data)
        if not match:
            return time.strftime('%Y-%m-%d H:i:s',time.localtime(time.time()))
        else:
            return match[0]


class EbrunNewsCrawler(Crawler):
    """
    亿邦动力 http://www.ebrun.com/search.php?keyword=%C3%C0%C0%F6%CB%B5&page=1
    """
    def __init__(self,keyword):
        """
        :param keyword:
        :return:
        """
        Crawler.__init__(self)
        if not keyword:
            raise RuntimeError('请提供搜索关键词')
        self.keyword = keyword
        self.api = 'http://www.ebrun.com/search.php?%s'
        #起始数据数据
        self.pn = 1
        #row number每行新闻的数量
        self.rn = 0
        self.logger = logger.get('opinion.crawler.EbrunNewsCrawler')
        self.headers = {
             'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0'
        }
        self.extract_pattern = r'<dl>.*?href="(.*?)".*?>(.*?)<\/a>.*?<span>(.*?)<\/span>(.*?)<\/dd>.*?class="line">'

    def read(self,pn=None,rn=None):
        """
        读取微博内容
        :param page: 页码
        :param count: 每页的微博数量
        :return:
        """
        #如果手动设置了要抓取的页面
        if pn is not None:
            self.pn = pn > 0 and pn or 0
        data = {
            'keyword':self.keyword.encode('GBK'),
            'page':self.pn,
        }
        params = urllib.urlencode(data)
        self.headers['Referer'] = self.api % (params)
        url = self.api % (params)
        #url= url.encode('gbk')
        #请求数据
        html = self.request(url,useProxy=True,headers=self.headers)
        #如果请求失败
        if html is None:
            self.logger.debug('抓取%s数据失败！' % url)
            return []

        content_regex = re.compile(r'<div class="select_tab">[\w\W]*<p class="pub_page01">')
        html_info = re.findall(content_regex,html)
        try:
            html = html_info[0]
        except Exception,e:
            self.logger.debug('正则匹配数据为空 %s 错误原因 %s' % (url,e))
            return []
        html = c_tool.tool_trim(html)
        regex = re.compile(self.extract_pattern)
        info =[]
        regex_match_all = re.findall(regex, html)
        if regex_match_all is None:
            self.logger.debug('%s,抓取%s数据失败！' % (self.keyword,url))
            return []
        for match in regex_match_all:
            if len(match) <4:
                continue
            try:
                info.append({
                    'url': match[0].decode('gbk').encode('utf-8'),
                    'title':c_tool.tool_strip_tag(match[1].decode('gbk').encode('utf-8')),
                    'summary':c_tool.tool_strip_tag(match[3].decode('gbk').encode('utf-8')),
                    'source':'亿邦动力',
                    'pub_date':match[2],
                })
            except Exception,e:
                 self.logger.debug('正则匹配数据错误 %s 错误原因 %s' % (url,e))
        #如果数据不正确
        if not info:
            self.logger.debug('%s 返回数据为空' % url)
            return []
        #自动进入下一页数据
        self.pn += 1
        #对微博的消息内容进行分析
        #return analysis(info,type='news_so360')
        return self.format(info)
    def format(self,n_list):
        """
        内容是使用正则提取的HTML，所以没有具体JSON格式
        :param n_list:
        :return:
        """
        new_list = []
        try:
            for m in n_list:
                if str(m['title'] + m['summary']).find('美丽说') == -1:
                    continue
                fmt = {}
                fmt['link'] = m['url']
                #取链接作为唯一标识
                fmt['unique_identify'] = fmt['link']
                fmt['title'] = m['title']
                fmt['summary'] =  m['summary']
                fmt['text_content'] = self.textFilter(m['title'] + m['summary'])
                fmt['source'] = '亿邦动力'
                fmt['type'] = 2 #新闻
                fmt['author'] = m['source']
                fmt['pub_date'] = m['pub_date']
                #额外记录该微博用户的信息
                fmt['json_data'] = {}
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化  亿邦动力 出错 %s ' % e )
        return new_list


class JIA365Crawler(Crawler):
    """
   365JIA.CN http://365jia.cn/search/?q=%E7%BE%8E%E4%B8%BD%E8%AF%B4&all=1&filter[
    0]=news&filter[1]=shop&filter[2]=product&filter[3]=house_post&filter[4]=fuwu&filter[5]=forum_thread&filter[6]=coupon&filter[7]=house&filter[8]=market&filter[9]=decor_market&filter[10]=ask&time_begin=&time_end=&author=&sort=time&page=2
    """
    def __init__(self,keyword):
        """
        :param keyword:
        :return:
        """
        Crawler.__init__(self)
        if not keyword:
            raise RuntimeError('请提供搜索关键词')
        self.keyword = keyword
        self.api = u'http://365jia.cn/search/?all=1&sort=time&%s&filter[]=%s'
        #起始数据数据
        self.pn = 1
        #row number每行新闻的数量
        self.rn = 0
        self.logger = logger.get('opinion.crawler.365JIACrawler')
        self.headers = {
             'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0'
        }
        self.extract_pattern_forum_thread = ur'<div class="tag">.*?<h3>.*?href=.*?>.*?href="(' \
                                ur'.*?)".*?>(.*?)<\/a>.*?<\/h3>.*?<span.*?>.*?(\d{1,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}).*?<\/span>'
        self.extract_pattern_news = ur'<div class="tag">.*?<h3>.*?href=.*?>.*?href="(.*?)".*?>(.*?)<\/a>.*?<\/h3>.*?<p>(.*?)<\/p>.*?<span class="cor_2">(.*?)<\/span>.*?<span.*?>.*?(\d{1,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}).*?<\/span>'

    def read(self,pn=None,rn=None):
        """
        读取微博内容
        :param page: 页码
        :param count: 每页的微博数量
        :return:
        """
        #如果手动设置了要抓取的页面
        if pn is not None:
            self.pn = pn > 0 and pn or 0
        filter = ['forum_thread','news']
        info =[]
        for filter_type in filter:
            data = {
                'q':self.keyword,
                'page':self.pn,
            }
            params = urllib.urlencode(data)
            self.headers['Referer'] = self.api % (params,filter_type)
            url = self.api % (params,filter_type)
            #url= url.encode('gbk')
            #请求数据
            html = self.request(url,useProxy=True,headers=self.headers)
            #如果请求失败
            if html is None:
                self.logger.debug('抓取%s数据失败！' % url)
                return []
            html = c_tool.tool_trim(html)
            if filter_type == 'forum_thread':
                regex = re.compile(self.extract_pattern_forum_thread)
                regex_match_all = re.findall(regex, html)
                if regex_match_all is None:
                    self.logger.debug('%s,抓取%s数据失败！' % (self.keyword,url))
                    return []
                for match in regex_match_all:
                    if len(match) <3:
                        continue
                    try:
                        info.append({
                            'url': match[0],
                            'title':c_tool.tool_strip_tag(match[1]),
                            'summary':c_tool.tool_strip_tag(match[1]),
                            'source':'365JIA.CN',
                            'pub_date':match[2],
                        })
                    except Exception,e:
                        self.logger.debug('正则匹配数据错误 %s 错误原因 %s' % (url,e))
            elif filter_type == 'news':
                regex = re.compile(self.extract_pattern_news)
                regex_match_all = re.findall(regex, html)
                if regex_match_all is None:
                    self.logger.debug('%s,抓取%s数据失败！' % (self.keyword,url))
                    return []
                for match in regex_match_all:
                     if len(match) <5:
                         continue
                     try:
                         info.append({
                            'url': match[0],
                            'title':c_tool.tool_strip_tag(match[1]),
                            'summary':c_tool.tool_strip_tag(match[2]),
                            'source':match[3],
                            'pub_date':match[4],

                         })
                     except Exception,e:
                        self.logger.debug('正则匹配数据错误 %s 错误原因 %s' % (url,e))
        #如果数据不正确
        if not info:
            self.logger.debug('%s 返回数据为空' % url)
            return []
        #自动进入下一页数据
        self.pn += 1
        #对微博的消息内容进行分析
        #return analysis(info,type='news_so360')
        return self.format(info)

    def format(self,n_list):
        """
        内容是使用正则提取的HTML，所以没有具体JSON格式
        :param n_list:
        :return:
        """
        new_list = []
        try:
            for m in n_list:
                if str(m['title'] + m['summary']).find('美丽说') == -1:
                    continue
                fmt = {}
                fmt['link'] = m['url']
                #取链接作为唯一标识
                fmt['unique_identify'] = fmt['link']
                fmt['title'] = m['title']
                fmt['summary'] =  m['summary']
                fmt['text_content'] = self.textFilter(m['title'] + m['summary'])
                fmt['source'] = '365JIA.CN'
                fmt['type'] = 2 #新闻
                fmt['author'] = m['source']
                fmt['pub_date'] = m['pub_date']
                #额外记录该微博用户的信息
                fmt['json_data'] = {}
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化  365JIA.CN 出错 %s ' % e )
        return new_list

class XinBaoNewsCrawler(Crawler):
    """
    新报
    http://www.xinbao.de/xinbao/e/search/result/?searchid=811
    """
    def __init__(self,keyword):
        """
        :param keyword:
        :return:
        """
        Crawler.__init__(self)
        if not keyword:
            raise RuntimeError('请提供搜索关键词')
        self.keyword = keyword
        self.api = 'http://www.xinbao.de/xinbao/e/search/index.php'
        self.host_url = 'http://www.xinbao.de'
        #起始数据数据
        self.pn = 1
        #row number每行新闻的数量
        self.rn = 0
        self.logger = logger.get('opinion.crawler.TOUSUO1forumCrawler')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.10 Safari/537.36',
             'Cookie':'__utma=156990514.968461404.1429160064.1429160064.1429515151.2; __utmz=156990514.1429160064.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmb=156990514.4.10.1429515151; __utmc=156990514; __utmt=1; jxdkpecookieinforecord=%2C61-511671%2C; jxdkpcheckplkey=1429515152%2Cfd797b6ae24f3b4ebd9ba8e2c09d8d08%2C5158; jxdkplastsearchtime=1429515225',

        }
        self.extract_pattern = r'<tr> <td id=.*?<span>.*?<\/span> <a href="(.*?)".*?>(.*?)<\/a><\/td>.*?<\/tr>.*?td.*?>(.*?)<\/td>.*?-.*?(\d{1,4}-\d{1,2}-\d{1,2})<\/span>.*?-.*?<a.*?>(.*?)<\/a>'
    def read(self,pn=None,rn=None):
        """
        读取微博内容
        :param page: 页码
        :param count: 每页的微博数量
        :return:
        """
        #如果手动设置了要抓取的页面
        if pn is not None:
            self.pn = pn > 0 and pn or 0
        data ={
            'tempid':'1',
            'x':0,
            'y':0,
            'tbname':'news',
            'show':'title',
            'keyboard':self.keyword.encode('gb2312')
        }

        url_params = urllib.urlencode(data)
        self.headers['Referer'] = self.api
        url = self.api
        #请求数据
        html = self.request(url,url_params,useProxy=True,headers=self.headers)
        #如果请求失败
        if html is None:
            self.logger.debug('抓取%s数据失败！' % url)
            return []
        html = c_tool.tool_trim(html)
        regex = re.compile(self.extract_pattern)
        info =[]

        regex_match_all = re.findall(regex, html)
        if regex_match_all is None:
            self.logger.debug('%s,抓取%s数据失败！' % (self.keyword,url))
            return []
        for match in regex_match_all:
            if len(match) <5:
                continue
            try:
                info.append({
                    'url': self.host_url + match[0].replace('&amp;','&'),
                    'title':c_tool.tool_strip_tag(match[1].decode('gb2312')),
                    'summary':c_tool.tool_strip_tag(match[2].decode('gb2312')),
                    'source':c_tool.tool_strip_tag(match[4].decode('gb2312')),
                    'pub_date':match[3]

                })
            except Exception,e:
                self.logger.debug('正则匹配数据错误 %s 错误原因 %s' % (url,e))
        #如果数据不正确
        if not info:
            self.logger.debug('%s 返回数据为空' % url)
            return []
        #自动进入下一页数据
        self.pn += 1
        #对微博的消息内容进行分析
        #return analysis(info,type='news_so360')
        return self.format(info)


    def format(self,n_list):
        """
        内容是使用正则提取的HTML，所以没有具体JSON格式
        :param n_list:
        :return:
        """
        new_list = []
        try:
            for m in n_list:
                if str(m['title'] + m['summary']).find('美丽说') == -1:
                    continue
                fmt = {}
                fmt['link'] = m['url']
                #取链接作为唯一标识
                fmt['unique_identify'] = fmt['link']
                fmt['title'] = m['title']
                fmt['summary'] =  m['summary']
                fmt['text_content'] = self.textFilter(m['title'] + m['summary'])
                fmt['source'] = '新报网'
                fmt['type'] = 2 #新报网
                fmt['author'] = m['source']
                fmt['pub_date'] = m['pub_date']
                #额外记录该微博用户的信息
                fmt['json_data'] = {}
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化 新报网 出错 %s ' % e )
        return new_list

class TaiZhouNewsCrawler(Crawler):
    """
    台州网
    http://www.taizhou.com.cn:8080/servlet/SearchServlet.do
    """
    def __init__(self,keyword):
        """
        :param keyword:
        :return:
        """
        Crawler.__init__(self)
        if not keyword:
            raise RuntimeError('请提供搜索关键词')
        self.keyword = keyword
        self.api = 'http://www.taizhou.com.cn:8080/servlet/SearchServlet.do'
        #起始数据数据
        self.pn = 1
        #row number每行新闻的数量
        self.rn = 0
        self.logger = logger.get('opinion.crawler.TaiZhouNewsCrawler')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.10 Safari/537.36',
        }
        self.extract_pattern = ur'<tr> <td align="left">.*?href="(.*?)".*?><span class="STYLE12">(' \
                               ur'.*?)<\/span><\/a><\/td>.*?class="STYLE3">(.*?)<\/span><\/td>'
    def read(self,pn=None,rn=None):
        """
        读取微博内容
        :param page: 页码
        :param count: 每页的微博数量
        :return:
        """
        #如果手动设置了要抓取的页面
        if pn is not None:
            self.pn = pn > 0 and pn or 0
        data ={
            'contentKey':self.keyword,
            'op':'single'
        }

        url_params = urllib.urlencode(data)
        self.headers['Referer'] = self.api
        url = self.api
        #请求数据
        html = self.request(url,url_params,useProxy=True,headers=self.headers)
        #如果请求失败
        if html is None:
            self.logger.debug('抓取%s数据失败！' % url)
            return []
        html = c_tool.tool_trim(html)
        regex = re.compile(self.extract_pattern)
        info =[]
        regex_match_all = re.findall(regex, html)
        if regex_match_all is None:
            self.logger.debug('%s,抓取%s数据失败！' % (self.keyword,url))
            return []
        for match in regex_match_all:
            if len(match) <3:
                continue
            try:
                info.append({
                    'url':  match[0],
                    'title':c_tool.tool_strip_tag(match[1]),
                    'summary':c_tool.tool_strip_tag(match[2]),
                    'source':'台州网',
                    'pub_date':self.analysis_time(match[0])

                })
            except Exception,e:
                    self.logger.debug('正则匹配数据错误 %s 错误原因 %s' % (url,e))
        #如果数据不正确
        if not info:
            self.logger.debug('%s 返回数据为空' % url)
            return []
        #自动进入下一页数据
        self.pn += 1
        #对微博的消息内容进行分析
        #return analysis(info,type='news_so360')
        return self.format(info)


    def format(self,n_list):
        """
        内容是使用正则提取的HTML，所以没有具体JSON格式
        :param n_list:
        :return:
        """
        new_list = []
        try:
            for m in n_list:
                if str(m['title'] + m['summary']).find('美丽说') == -1:
                    continue
                fmt = {}
                fmt['link'] = m['url']
                #取链接作为唯一标识
                fmt['unique_identify'] = fmt['link']
                fmt['title'] = m['title']
                fmt['summary'] =  m['summary']
                fmt['text_content'] = self.textFilter(m['title'] + m['summary'])
                fmt['source'] = '中国台州网'
                fmt['type'] = 2 #新报网
                fmt['author'] = m['source']
                fmt['pub_date'] = m['pub_date']
                #额外记录该微博用户的信息
                fmt['json_data'] = {}
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化 中国台州网 出错 %s ' % e )
        return new_list

      #解析时间返回需要的时间
    def analysis_time(self,data):
        #02月28日 17:22
        content_regex = re.compile(r'(\d{1,4}-\d{1,2}\/\d{1,2})')
        match = re.findall(content_regex, data)
        if not match:
            return time.strftime('%Y-%m-%d H:i:s',time.localtime(time.time()))
        else:
            return match[0]

class AnHuiNewsCrawler(Crawler):
    """
    中安在线
    http://search.anhuinews.com:7001/m_fullsearch/full_search.jsp
    """
    def __init__(self,keyword):
        """
        :param keyword:
        :return:
        """
        Crawler.__init__(self)
        if not keyword:
            raise RuntimeError('请提供搜索关键词')
        self.keyword = keyword
        self.api = 'http://search.anhuinews.com:7001/m_fullsearch/full_search.jsp'
        #起始数据数据
        self.pn = 0
        #row number每行新闻的数量
        self.rn = 20
        self.logger = logger.get('opinion.crawler.AnHuiNewsCrawler')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.10 Safari/537.36',
        }
        self.extract_pattern = r'<tr>.*?class="searchTitle"><a.*?href="(.*?)">(.*?)<\/a>.*?class="searchMain">(.*?)<\/td>.*?class="searchBotton">.*?(\d{1,4}-\d{1,2}-\d{1,2})<br>'
    def read(self,pn=None,rn=None):
        """
        读取微博内容
        :param page: 页码
        :param count: 每页的微博数量
        :return:
        """
        #如果手动设置了要抓取的页面
        if pn is not None:
            self.pn = pn > 0 and pn or 0
        data ={
            'keywords':self.keyword.encode('gb2312'),
            'sort':'2',
            'size': self.rn,
            'pagen':self.pn
        }

        url_params = urllib.urlencode(data)
        self.headers['Referer'] = self.api
        url = self.api
        #请求数据
        html = self.request(url,url_params,useProxy=True,headers=self.headers)
        #如果请求失败
        if html is None:
            self.logger.debug('抓取%s数据失败！' % url)
            return []
        html = c_tool.tool_trim(html)
        regex = re.compile(self.extract_pattern)
        info =[]
        regex_match_all = re.findall(regex, html)
        if regex_match_all is None:
            self.logger.debug('%s,抓取%s数据失败！' % (self.keyword,url))
            return []
        for match in regex_match_all:
            if len(match) <4:
                continue
            try:
                info.append({
                    'url':  match[0],
                    'title':c_tool.tool_strip_tag(match[1].decode('gb2312')),
                    'summary':c_tool.tool_strip_tag(match[2].decode('gb2312')),
                    'source':'安徽新闻',
                    'pub_date':match[3]

                })
            except Exception,e:
                self.logger.debug('正则匹配数据错误 %s 错误原因 %s' % (url,e))
        #如果数据不正确
        if not info:
            self.logger.debug('%s 返回数据为空' % url)
            return []
        #自动进入下一页数据
        self.pn += 1
        #对微博的消息内容进行分析
        #return analysis(info,type='news_so360')
        return self.format(info)


    def format(self,n_list):
        """
        内容是使用正则提取的HTML，所以没有具体JSON格式
        :param n_list:
        :return:
        """
        new_list = []
        try:
            for m in n_list:
                if str(m['title'] + m['summary']).find('美丽说') == -1:
                    continue
                fmt = {}
                fmt['link'] = m['url']
                #取链接作为唯一标识
                fmt['unique_identify'] = fmt['link']
                fmt['title'] = m['title']
                fmt['summary'] =  m['summary']
                fmt['text_content'] = self.textFilter(m['title'] + m['summary'])
                fmt['source'] = '安徽新闻'
                fmt['type'] = 2 #新报网
                fmt['author'] = m['source']
                fmt['pub_date'] = m['pub_date']
                #额外记录该微博用户的信息
                fmt['json_data'] = {}
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化 安徽新闻 出错 %s ' % e )
        return new_list

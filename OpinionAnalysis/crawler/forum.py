#!/usr/bin/env python
# coding: utf-8
#论坛类
__author__ = 'guojiezhu'


import json
import re
import time
import urllib
from .crawler import Crawler
from . import logger
import  zlib
from . import  c_tool

class ZuanKe8Crawler(Crawler):
    """
    赚客8 http://www.zuanke8.com/forum.php?mod=viewthread&tid=1920296#lastpost
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
        self.api = u'http://zhannei.baidu.com/cse/search?q=%s&p=%s&s=1094671438589733301&srt=cse_createTime'
        #起始数据数据
        self.pn = 0
        #row number每行新闻的数量
        self.rn = 0
        self.logger = logger.get('opinion.crawler.ZuanKe8forumCrawler')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:37.0) Gecko/20100101 Firefox/37.0'

        }
        self.extract_pattern = r'<div class="result f s3">.*?href="(.*?)" .*?>(.*?)<\/a>.*?class="c-abstract">(.*?)<\/div>.*?<\/div>.*?<\/div>.*?<div class="c-summary-1"><span>来自：(.*?)<\/span><span>作者：(.*?)<\/span><span>发布：(.*?)<\/span>'
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
        html = c_tool.tool_trim(html)
        regex = re.compile(self.extract_pattern)
        info =[]
        regex_match_all = re.findall(regex, html)
        if regex_match_all is None:
            self.logger.debug('%s,抓取%s数据失败！' % (self.keyword,url))
            return info
        for match in regex_match_all:
            if len(match) <6:
                continue
            try:
                info.append({
                    'url': match[0].decode('utf-8'),
                    'title':c_tool.tool_strip_tag(match[1].decode('utf-8')),
                    'summary':c_tool.tool_strip_tag(match[2].decode('utf-8')),
                    'source':match[4].decode('utf-8'),
                    'pub_date':match[5],

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
                fmt['source'] = '赚客8'
                fmt['type'] = 4 #论坛
                fmt['author'] = m['source']
                fmt['pub_date'] = m['pub_date']+" 00:00:00"
                #额外记录该微博用户的信息
                fmt['json_data'] = {}
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化 赚客8 出错 %s ' % e )
        return new_list

class DAYOOCrawler(Crawler):
    """
    大洋网http://zhannei.baidu.com/cse/search?q=%E7%BE%8E%E4%B8%BD%E8%AF%B4&s=12590748706517226876&srt=lds&nsid=1
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
        self.api = u'http://zhannei.baidu.com/cse/search?q=%s&p=%s&&s=12590748706517226876&srt=lds&nsid=1'
        #起始数据数据
        self.pn = 1
        #row number每行新闻的数量
        self.rn = 0
        self.logger = logger.get('opinion.crawler.DAYOOforumCrawler')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:37.0) Gecko/20100101 Firefox/37.0'

        }
        self.extract_pattern = ur'<div class="result.*?href="(.*?)".*?>(.*?)<\/a>.*?class="c-abstract" >(' \
                               ur'.*?)<\/div>.*?class="c-showurl".*?(\d{1,4}-\d{1,2}-\d{1,2})<\/span> '
    def read(self,pn=None,rn=None):
        """
        读取微博内容
        :param page: 页码
        :param count: 每页的微博数量
        :return:
        """
        #如果手动设置了要抓取的页面
        self.headers['Referer'] = self.api % (self.keyword, self.pn-1)
        url = self.api % (self.keyword,self.pn-1)

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
                    'source':'大洋网',
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
                if str(m['title'] + m['summary']).find('美丽说') == -1:
                    continue
                fmt = {}
                fmt['link'] = m['url']
                #取链接作为唯一标识
                fmt['unique_identify'] = fmt['link']
                fmt['title'] = m['title']
                fmt['summary'] =  m['summary']
                fmt['text_content'] = self.textFilter(m['title'] + m['summary'])
                fmt['source'] = '大洋网'
                fmt['type'] = 4 #论坛
                fmt['author'] = m['source']
                fmt['pub_date'] = m['pub_date']+" 00:00:00"
                #额外记录该微博用户的信息
                fmt['json_data'] = {}
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化 大洋网 出错 %s ' % e )
        return new_list


class WY163Crawler(Crawler):
    """
    http://bbs.163.com/bbs/search.do?boardid=gonglue&orderbytime=n&q=%E7%BE%8E%E4%B8%BD%E8%AF%B4&searchType=title&searchRan=bbs
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
        self.api = u'http://bbs.163.com/bbs/search.do?boardid=gonglue&orderbytime=n&q=%s&searchType=title&searchRan=bbs&pageid=%s'
        #起始数据数据
        self.pn = 0
        #row number每行新闻的数量
        self.rn = 0
        self.logger = logger.get('opinion.crawler.WY163forumCrawler')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:37.0) Gecko/20100101 Firefox/37.0',
        }
        self.extract_pattern = ur'<div.*?href="(.*?)" target="_blank">(.*?)<\/a>.*?\[(.*?)\]<\/span>.*?class="textA">(.*?)<\/div>.*?class="relate">.*?target="_blank">(.*?)<\/a>'
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
        self.headers['Referer'] = self.api % (self.keyword, self.pn)

        url = self.api % (self.keyword,self.pn)

        #请求数据
        html = self.request(url,useProxy=True,headers=self.headers)
        #如果请求失败
        if html is None:
            self.logger.debug('抓取%s数据失败！' % url)
            return []
        html = c_tool.tool_trim(html)
        # f = open('./tmp/text.txt','w')
        # f.write(html)
        # exit()
        regex = re.compile(self.extract_pattern)
        info =[]
        regex_match_all = re.findall(regex, html)
        if regex_match_all is None:
            self.logger.debug('%s,抓取%s数据失败！' % (self.keyword,url))
            return info
        for match in regex_match_all:
            if len(match) <5:
                continue
            try:
                info.append({
                    'url': match[0],
                    'title':c_tool.tool_strip_tag(match[1]),
                    'summary':c_tool.tool_strip_tag(match[3]),
                    'source':match[4],
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
                fmt['source'] = '网易论坛'
                fmt['type'] = 4 #论坛
                fmt['author'] = m['source']
                fmt['pub_date'] = m['pub_date']
                #额外记录该微博用户的信息
                fmt['json_data'] = {}
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化 网易论坛 出错 %s ' % e )
        return new_list


class G8F8Crawler(Crawler):
    """
    高峰论坛
    http://www.g8f8.com/search.php?mod=forum&searchid=4&orderby=lastpost&ascdesc=desc&searchsubmit=yes&page=2&kw=
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
        self.api = 'http://www.g8f8.com/search.php?mod=forum'
        self.local_url = 'http://www.g8f8.com/'
        #起始数据数据
        self.pn = 1
        #row number每行新闻的数量
        self.rn = 0
        self.logger = logger.get('opinion.crawler.G8F8forumCrawler')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.10 Safari/537.36',
             'Cookie':'HUUk_2132_saltkey=fVxOo3vx; HUUk_2132_lastvisit=1429010110; HUUk_2132_pvi=408652173; pos=null; sid=null; '
                     'HUUk_2132_sid=cLh95B; pgv_pvi=3485944017; pgv_info=ssi=s9608638280; Hm_lvt_23b8da0713994067ed9afd912d4407d3=1429013711,1429504090; Hm_lpvt_23b8da0713994067ed9afd912d4407d3=1429504743; HUUk_2132_lastact=1429504743%09plugin.php%09',

        }
        self.extract_pattern = r'<li class="pbw".*?href="(.*?)".*?>(.*?)<\/a>.*?<p.*?<p>(.*?)<\/p>.*?<span>(.*?)<\/span>.*?href=.*?>(.*?)<\/a>'
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
            'formhash':'298f587b',
            'searchsubmit':'yes',
            #'srchtype':'fulltext',
            'srchtxt':self.keyword.encode('gbk')
        }

        url_params = urllib.urlencode(data)
        self.headers['Referer'] = self.api
        url = self.api
        #请求数据
        redirect_url = self.request_response(url,url_params,useProxy=True,headers=self.headers)
        if redirect_url is None:
            self.logger.debug('抓取%s数据失败！' % url)
            return []

        redirect_url = redirect_url.replace('orderby=lastpost','orderby=dateline')
        html = self.request(redirect_url,useProxy=True,headers=self.headers)
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
            return info
        for match in regex_match_all:
            if len(match) <5:
                continue
            try:
                info.append({
                    'url': self.local_url+match[0].replace('&amp;','&'),
                    'title':c_tool.tool_strip_tag(match[1].decode('gbk')),
                    'summary':c_tool.tool_strip_tag(match[2].decode('gbk')),
                    'source':c_tool.tool_strip_tag(match[4].decode('gbk')),
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
                if str(m['title'] + m['summary']).find('美丽说') == -1:
                    continue
                fmt = {}
                fmt['link'] = m['url']
                #取链接作为唯一标识
                fmt['unique_identify'] = fmt['link']
                fmt['title'] = m['title']
                fmt['summary'] =  m['summary']
                fmt['text_content'] = self.textFilter(m['title'] + m['summary'])
                fmt['source'] = '高峰论坛'
                fmt['type'] = 4 #论坛
                fmt['author'] = m['source']
                fmt['pub_date'] = m['pub_date']
                #额外记录该微博用户的信息
                fmt['json_data'] = {}
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化 高峰论坛 出错 %s ' % e )
        return new_list

class TouSuCrawler(Crawler):
    """
    投诉哦易
  http://www.tousu1.com/forum.php?mod=viewthread&tid=50935&extra=page=1&filter=lastpost&orderby=lastpost
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
        self.api = 'http://www.tousu1.com/search.php?mod=forum'
        self.local_url = 'http://www.tousu1.com/'
        #起始数据数据
        self.pn = 1
        #row number每行新闻的数量
        self.rn = 0
        self.logger = logger.get('opinion.crawler.TOUSUO1forumCrawler')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.10 Safari/537.36',
             'Cookie':'1jol_2132_saltkey=XnYHtu00; 1jol_2132_lastvisit=1429078253; 1jol_2132_visitedfid=38; AJSTAT_ok_times=3; bdshare_firstime=1429083392390; 1jol_2132_sid=byy9EC; 1jol_2132_lastact=1429510369%09search.php%09forum; 1jol_2132_st_p=0%7C1429510229%7C41266d5ccbfdb686b46ffe8066aeccd6; 1jol_2132_viewid=tid_50935; AJSTAT_ok_pages=4; 1jol_2132_sendmail=1',

        }
        self.extract_pattern = r'<li class="pbw".*?href="(.*?)".*?>(.*?)<\/a>.*?<p.*?<p>(.*?)<\/p>.*?<span>(.*?)<\/span>.*?href=.*?>(.*?)<\/a>'
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
            'formhash':'3c460be8',
            'searchsubmit':'yes',
            #'srchtype':'fulltext',
            'srchtxt':self.keyword.encode('gbk')
        }

        url_params = urllib.urlencode(data)
        self.headers['Referer'] = self.api
        url = self.api
        #请求数据
        redirect_url = self.request_response(url,url_params,useProxy=True,headers=self.headers)
        if redirect_url is None:
            self.logger.debug('抓取%s数据失败！' % url)
            return []

        redirect_url = redirect_url.replace('orderby=lastpost','orderby=dateline')
        html = self.request(redirect_url,useProxy=True,headers=self.headers)
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
            return info
        for match in regex_match_all:
            if len(match) <5:
                continue
            try:
                info.append({
                    'url': match[0].replace('&amp;','&'),
                    'title':c_tool.tool_strip_tag(match[1].decode('gbk')),
                    'summary':c_tool.tool_strip_tag(match[2].decode('gbk')),
                    'source':c_tool.tool_strip_tag(match[4].decode('gbk')),
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
                if str(m['title'] + m['summary']).find('美丽说') == -1:
                    continue
                fmt = {}
                fmt['link'] = m['url']
                #取链接作为唯一标识
                fmt['unique_identify'] = fmt['link']
                fmt['title'] = m['title']
                fmt['summary'] =  m['summary']
                fmt['text_content'] = self.textFilter(m['title'] + m['summary'])
                fmt['source'] = '投诉易'
                fmt['type'] = 4 #论坛
                fmt['author'] = m['source']
                fmt['pub_date'] = m['pub_date']
                #额外记录该微博用户的信息
                fmt['json_data'] = {}
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化 投诉易 出错 %s ' % e )
        return new_list

class SinaBlogCrawler(Crawler):

    def __init__(self,keyword):
        """
        新浪博客
        http://site.proc.sina.cn/search/blog_search.php?keyword=%E7%BE%8E%E4%B8%BD%E8%AF%B4&vt=4&page=1&range=title&from=null&type=%E5%8D%9A%E6%96%87&vt=4
        :param keyword:
        :return:
        """
        Crawler.__init__(self)
        if not keyword:
            raise RuntimeError('请提供搜索关键词')
        self.keyword = keyword
        self.api ='http://search.sina.com.cn/?%s&c=blog&col=&range=&source=&from=&country=&size=&time=&a=&page=%s&dpc=1'
        #起始数据数据
        self.pn = 1
        #row number每行新闻的数量
        self.rn = 20
        self.logger = logger.get('opinion.crawler.SinaBlogforumCrawler')
        self.headers = {

            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:37.0) Gecko/20100101 Firefox/37.0'
        }
        self.extract_pattern =r'<div.*?class="box-result.*?href="(.*?)">(.*?)<\/a>.*?class="content">(.*?)<\/p>.*?class="fgray_time">(.*?)<\/span><span.*?"fgray">.*?href=.*?>(.*?)<\/a>'

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
        #self.keyword ='美丽说垃圾'
        data = {
            'q':self.keyword.encode('gb2312')
        }

        params = urllib.urlencode(data)
        self.headers['Referer'] = self.api % (params,self.pn)
        url = self.api % (params,self.pn)
        #请求数据
        html = self.request(url,useProxy=True,headers=self.headers)
        html = c_tool.tool_trim(html)
        regex = re.compile(self.extract_pattern)
        info = []
        regex_match_all = re.findall(regex, html)
        if regex_match_all is None:
            self.logger.debug('%s,抓取%s数据失败！' % (self.keyword,url))
            return info

        for match in regex_match_all:
            if len(match) <5:
                continue
            try:
                info.append({
                    'url': match[0],
                    'title':c_tool.tool_strip_tag(match[1]),
                    'summary':c_tool.tool_strip_tag(match[2]),
                    'author':match[4],
                    'pub_date':match[3],
                })
            except Exception,e:
                self.logger.debug('正则匹配数据错误 %s 错误原因 %s' % (url,e))
            #exit()
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
        new_list = []
        try:
            for m in n_list:
                if str(c_tool.tool_strip_tag(m['title'] + m['summary'])).find('美丽说') == -1:
                    continue
                fmt = {}
                fmt['unique_identify'] =  m['url']
                fmt['title'] = m['title']
                fmt['summary'] =  m['summary']
                fmt['text_content'] = self.textFilter(m['title'] + m['summary'])
                fmt['source'] = '新浪博客'
                fmt['type'] = 4 #博客
                fmt['author'] = m['author']
                fmt['link'] = m['url']
                fmt['pub_date'] = m['pub_date']
                #额外记录该微博用户的信息
                fmt['json_data'] = {}
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化 新浪博客 出错 %s ' % e )
        return new_list

class MAMACrawler(Crawler):

    def __init__(self,keyword):
        """
        妈妈圈
        http://q.mama.cn/search/topic.html?q=%E7%BE%8E%E4%B8%BD%E8%AF%B4&p=1
        """
        Crawler.__init__(self)
        if not keyword:
            raise RuntimeError('请提供搜索关键词')
        self.keyword = keyword
        self.api = 'http://q.mama.cn/search/topic.html?%s'
        #起始数据数据
        self.pn = 1
        #row number每行新闻的数量
        self.rn = 20
        self.logger = logger.get('opinion.crawler.MAMACrawler')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:37.0) Gecko/20100101 Firefox/37.0'
        }
        self.extract_pattern = r'<dl>.*?href="(.*?)" title="(.*?)">.*?class="timebar"><span>.*?<\/span><span>(.*?)<\/span>.*?href=".*?">(.*?)<\/a><\/span>'

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
        # content_regex = re.compile(r'\r\n+')
        # html = re.sub(content_regex,'',html)
        regex = re.compile(self.extract_pattern)
        info =[]
        regex_match_all = re.findall(regex, html)
        if regex_match_all is None:
            self.logger.debug('%s,抓取%s数据失败！' % (self.keyword,url))
            return info
        for match in regex_match_all:
            if len(match) <4:
                continue
            try:
                info.append({
                    'url': match[0],
                    'title':c_tool.tool_strip_tag(match[1]),
                    'summary':c_tool.tool_strip_tag(match[1]),
                    'author':match[3],
                    'pub_date':self.analysis_time(match[2])
                })
            except Exception,e:
                self.logger.debug('正则匹配数据错误 %s 错误原因 %s' % (url,e))
        #如果请求失败
        if info is None:
            self.logger.debug('抓取%s数据失败！' % url)
            return []
        #第一页抓取到的是html
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
        new_list = []
        try:
            for m in n_list:
                if str(m['title'] + m['summary']).find('美丽说') == -1:
                    continue
                fmt = {}
                fmt['unique_identify'] =  m['url']
                fmt['title'] = m['title']
                fmt['summary'] =  m['summary']
                fmt['text_content'] = self.textFilter(m['title'])
                fmt['source'] = '妈妈圈'
                fmt['type'] = 4 #新闻
                fmt['author'] = m['author']
                fmt['link'] = m['url']
                fmt['pub_date'] = m['pub_date']
                #额外记录该微博用户的信息
                fmt['json_data'] = {}
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化 妈妈圈 出错 %s ' % e )
        return new_list

    #解析时间返回需要的时间
    def analysis_time(self,data):
        #02月28日 17:22
        content_regex = re.compile(r'(\d{1,2})月(\d{1,2})日\s(\d{1,2}:\d{1,2})')
        match = re.findall(content_regex, data)
        if not match:
            return data
        else:
            now_year = time.strftime('%Y',time.localtime(time.time()))
            return '%s-%s-%s %s' %(now_year,match[0][0],match[0][1],match[0][2])

class IfengCrawler(Crawler):

    def __init__(self,keyword):
        """
        凤凰网
        http://search.ifeng.com/sofeng/search.action?q=%E7%BE%8E%E4%B8%BD%E8%AF%B4&c=1&p=2
        """
        Crawler.__init__(self)
        if not keyword:
            raise RuntimeError('请提供搜索关键词')
        self.keyword = keyword
        self.api = 'http://search.ifeng.com/sofeng/search.action?%s&c=1'
        #起始数据数据
        self.pn = 1
        #row number每行新闻的数量
        self.rn = 20
        self.logger = logger.get('opinion.crawler.IfengforumCrawler')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:37.0) Gecko/20100101 Firefox/37.0'
        }
        self.extract_pattern = ur'<div class="searchResults">.*?href="(.*?)" target="_blank">(.*?)<\/a>(' \
                               ur'.*?)<font color="#1a7b2e"> (.*?) (\d{1,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})<\/font>'

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
        html = c_tool.tool_trim(html)
        regex = re.compile(self.extract_pattern)
        info =[]
        regex_match_all = re.findall(regex, html)
        if regex_match_all is None:
            self.logger.debug('%s,抓取%s数据失败！' % (self.keyword,url))
            return info
        for match in regex_match_all:
            if len(match) <5:
                continue
            try:
                info.append({
                    'url': match[0],
                    'title':c_tool.tool_strip_tag(match[1]),
                    'summary':c_tool.tool_strip_tag(match[2]),
                    'author':match[3],
                    'pub_date':match[4]

                 })
            except Exception,e:
                self.logger.debug('正则匹配数据错误 %s 错误原因 %s' % (url,e))
        #如果请求失败
        if info is None:
            self.logger.debug('抓取%s数据失败！' % url)
            return []
        #自动进入下一页数据
        self.pn += self.rn
        #对微博的消息内容进行分析
        #return analysis(info,type='baidu_news')
        return self.format(info)

    def format(self,n_list):
        new_list = []
        try:
            for m in n_list:
                if str(m['title'] + m['summary']).find('美丽说') == -1:
                    continue
                fmt = {}
                fmt['unique_identify'] =  m['url']
                fmt['title'] = m['title']
                fmt['summary'] =  m['summary']
                fmt['text_content'] = self.textFilter(m['title']+m['summary'])
                fmt['source'] = '凤凰网'
                fmt['type'] = 4 #新闻
                fmt['author'] = m['author']
                fmt['link'] = m['url']
                fmt['pub_date'] = m['pub_date']
                #额外记录该微博用户的信息
                fmt['json_data'] = {}
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化 凤凰网 出错 %s ' % e )
        return new_list

#CCTV 网页和博客
class CCTVCrawler(Crawler):

    def __init__(self,keyword):
        """
        cctv
        http://search.cctv.com/search.php?%s&type=web&datepid=1&vtime=-1&sort=date
        """
        Crawler.__init__(self)
        if not keyword:
            raise RuntimeError('请提供搜索关键词')
        self.keyword = keyword
        self.api = 'http://search.cctv.com/search.php?%s&type=%s&datepid=1&vtime=-1' \
                   '&sort=date'
        #起始数据数据
        self.pn = 1
        #row number每行新闻的数量
        self.rn = 20
        self.logger = logger.get('opinion.crawler.CCTVforumCrawler')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:37.0) Gecko/20100101 Firefox/37.0'
        }
        self.extract_pattern = r'<li>.*?href="(.*?)" target="_blank">(.*?)<\/a><\/h3><p>(.*?)<\/p><span style="float:left">来源：(.*?)<\/span><span style="float:right">发布时间：(.*?)<\/span><\/li>'

    def read(self,pn=None,rn=None):
        """
        读取微博内容
        :param page: 页码
        :param count: 每页的微博数量
        :return:
        """
        #如果手动设置了要抓取的页面
        type_tump  =['web','blog']
        info =[]
        for type in type_tump:
            info.extend( self.parse_html(self.pn,type))
        #自动进入下一页数据
        self.pn += self.rn
        #对微博的消息内容进行分析
        #return analysis(info,type='baidu_news')
        return self.format(info)

    def parse_html(self,pn=None,type='web'):
        data = {
            'qtext':self.keyword,
            'page':pn
        }
        params = urllib.urlencode(data)
        self.headers['Referer'] = self.api % (params,type)
        url = self.api % (params,type)
        #请求数据
        html = self.request(url,useProxy=True,headers=self.headers)
        regex = re.compile(self.extract_pattern)
        parse_info =[]
        regex_match_all = re.findall(regex, html)
        if regex_match_all is None:
            self.logger.debug('%s,抓取%s数据失败！' % (self.keyword,url))
            return parse_info
        for match in regex_match_all:
            if len(match) <5:
                continue
            try:
                parse_info.append({
                    'url': match[0],
                    'title':c_tool.tool_strip_tag(match[1]),
                    'summary':c_tool.tool_strip_tag(match[2]),
                    'author':match[3],
                    'pub_date':match[4]
                })
            except Exception,e:
                self.logger.debug('正则匹配数据错误 %s 错误原因 %s' % (url,e))
        #如果请求失败
        if parse_info is None:
            self.logger.debug('抓取%s数据失败！' % url)
            return []
        return parse_info


    def format(self,n_list):
        new_list = []
        try:
            for m in n_list:
                if str(m['title'] + m['summary']).find('美丽说') == -1:
                    continue
                fmt = {}
                fmt['unique_identify'] =  m['url']
                fmt['title'] = m['title']
                fmt['summary'] =  m['summary']
                fmt['text_content'] = self.textFilter(m['title']+m['summary'])
                fmt['source'] = 'CCTV央视网'
                fmt['type'] = 4 #新闻
                fmt['author'] = m['author']
                fmt['link'] = m['url']
                fmt['pub_date'] = m['pub_date']
                #额外记录该微博用户的信息
                fmt['json_data'] = {}
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化 CCTV央视网 出错 %s ' % e )
        return new_list

class TaoBaoBBSCrawler(Crawler):

    def __init__(self,keyword):
        """
        凤凰网
        http://bbs.taobao.com/search/thread.htm?spm=0.0.0.0.1GqYzl&q=%C3%C0%C0%F6%CB%B5&condition=post&order=1
        """
        Crawler.__init__(self)
        if not keyword:
            raise RuntimeError('请提供搜索关键词')
        self.keyword = keyword
        self.api = 'http://bbs.taobao.com/search/thread.htm?spm=0.0.0.0.0H5zfP&%s&condition=post&order=1'
        #起始数据数据
        self.pn = 1
        #row number每行新闻的数量
        self.rn = 20
        self.logger = logger.get('opinion.crawler.TAOBOBBSforumCrawler')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:37.0) Gecko/20100101 Firefox/37.0'
        }
        self.extract_pattern = r'class="subject">.*?href="(.*?)".*?">(.*?)<\/a>.*?class="belong">.*?"_blank">(.*?)<\/a>.*?<div class="name">.*?>(.*?)<\/a>.*?class="time">(.*?)<\/div>'

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
                'q':self.keyword.encode('GBK')
        }

        params = urllib.urlencode(data)
        self.headers['Referer'] = self.api % (params)
        url = self.api % (params)
        #请求数据
        html = self.request(url,useProxy=True,headers=self.headers)
        html = c_tool.tool_trim(html)
        regex = re.compile(self.extract_pattern)
        info =[]
        regex_match_all = re.findall(regex, html)
        if regex_match_all is None:
            self.logger.debug('%s,抓取%s数据失败！' % (self.keyword,url))
            return info
        for match in regex_match_all:
            if len(match) < 5:
                continue
            try:
                info.append({
                    'url': match[0],
                    'title':c_tool.tool_strip_tag(match[1]).decode('GBK'),
                    'summary':c_tool.tool_strip_tag(match[1]).decode('GBK'),
                    'author':match[3].decode('GBK'),
                    'pub_date':self.format_time( match[4] )
                })
            except Exception,e:
                self.logger.debug('正则匹配数据错误 %s 错误原因 %s' % (url,e))

        #如果请求失败
        if info is None:
            self.logger.debug('抓取%s数据失败！' % url)
            return []
        #自动进入下一页数据
        self.pn += self.rn
        #对微博的消息内容进行分析
        #return analysis(info,type='baidu_news')
        return self.format(info)

    def format(self,n_list):
        new_list = []
        try:
            for m in n_list:
                if str(m['title'] + m['summary']).find('美丽说') == -1:
                    continue
                fmt = {}
                fmt['unique_identify'] =  m['url']
                fmt['title'] = m['title']
                fmt['summary'] =  m['summary']
                fmt['text_content'] = self.textFilter(m['title']+m['summary'])
                fmt['source'] = '淘宝论坛'
                fmt['type'] = 4 #新闻
                fmt['author'] = m['author']
                fmt['link'] = m['url']
                fmt['pub_date'] = m['pub_date']
                #额外记录该微博用户的信息
                fmt['json_data'] = {}
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化 淘宝论坛 出错 %s ' % e )
        return new_list

    def format_time(self,data):
        if re.match(r'(\d{1,4}-\d{1,4}-\d{1,4})',data):
            return data
        else :
            return time.strftime('%Y-%m-%d',time.localtime(time.time()))


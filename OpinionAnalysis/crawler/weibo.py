#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import re
import random
import base64
import urllib

from .crawler import Crawler
from . import logger

class WeiboCrawler(Crawler):
    """
    新浪微博爬虫
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
        self.api = 'http://m.weibo.cn/searchs/weibo?%s'
        self.page = 1
        self.count = 50
        self.logger = logger.get('opinion.crawler.WeiboCrawler')


    def read(self,page=None,count=None):
        """
        读取微博内容
        :param page: 页码
        :param count: 每页的微博数量
        :return:
        """
        #如果手动设置了要抓取的页面
        if page is not None:
            self.page = page > 0 and page or 1
        if count is not None:
            self.count = count > 0 and count or 50

        #抓取地址可以翻页
        params = urllib.urlencode({"key":self.keyword,"page":self.page,"count":self.count})
        url = self.api % params

        #请求数据
        result = self.request(url,useProxy=True)
        #如果请求失败
        if result is None:
            self.logger.debug('抓取%s数据失败！' % url)
            #raise StopIteration()
            return []
        try:
            info = json.loads(result)
        except Exception,e:
            self.logger.error('格式化 新浪微博JSON数据格式 出错 %s ' % e )
            return []
        #如果数据不正确
        if info['ok'] == 0 or not info['mblogList']:
            self.logger.debug('%s 返回数据不正确!' % url)
            #raise StopIteration()
            return []

        #自动进入下一页数据
        self.page += 1
        #对微博的消息内容进行分析
        #return analysis(info['mblogList'],type='weibo')
        #yield self.format(info['mblogList'])
        return self.format(info['mblogList'])

    def format(self,m_list):
        """
        格式化微博内容为统一的格式
        其中微博消息的格式
        {
    "created_at": "1分钟前",
    "id": 3778672634811934,
    "mid": "3778672634811934",
    "idstr": "3778672634811934",
    "text": "<a class=\"k\" href=\"/k/%E9%9F%A9%E5%9B%BD%E4%BC%AF%E7%88%B5.%E7%BE%8E%E4%B8%BD%E8%AF%B4?from=feed\">#韩国伯爵.美丽说#</a> 人生都要遇见四个人，第一个是你爱但不爱你的人，第二个是爱你但你不爱的人，第三个是你爱又爱你但最后不能在一起的人，第四个是你未必爱但最后在一起的人。 <i class=\"face face_2 icon_24\">[心]</i>喜欢就关注北京韩国伯爵婚纱摄影",
    "source_type": 1,
    "source": "微博 weibo.com",
    "favorited": false,
    "pic_ids": [
        "005KKCSRtw1emf8ptfm1qj307r0cqq3d",
        "005KKCSRtw1emf8pu0zrij306m08taao",
        "005KKCSRtw1emf8purir7j30a40btaat",
        "005KKCSRtw1emf8pvegrjj30a50drjs2"
    ],
    "thumbnail_pic": "http://ww2.sinaimg.cn/thumbnail/005KKCSRtw1emf8ptfm1qj307r0cqq3d.jpg",
    "bmiddle_pic": "http://ww2.sinaimg.cn/bmiddle/005KKCSRtw1emf8ptfm1qj307r0cqq3d.jpg",
    "original_pic": "http://ww2.sinaimg.cn/large/005KKCSRtw1emf8ptfm1qj307r0cqq3d.jpg",
    "user": {
        "id": 5271488177,
        "screen_name": "伯爵定制婚纱摄影",
        "profile_image_url": "http://tp2.sinaimg.cn/5271488177/50/22885064745/1",
        "profile_url": "/u/5271488177",
        "statuses_count": 502,
        "verified": true,
        "remark": "",
        "verified_type": 2,
        "gender": "m",
        "mbtype": 0,
        "h5icon": {
            "main": "http://u1.sinaimg.cn/upload/2013/02/22/v_blue_2x.png",
            "other": []
        },
        "ismember": 0,
        "valid": null,
        "fansNum": 51506,
        "follow_me": false,
        "following": false
    },
    "reposts_count": 0,
    "comments_count": 0,
    "attitudes_count": 0,
    "mlevel": 0,
    "visible": {
        "type": 0,
        "list_id": 0
    },
    "darwin_tags": [],
    "status": 0,
    "relation": "0",
    "category": 31,
    "base62_id": "Bx0DlkbNQ",
    "attitudes_status": 0,
    "topic_struct": [
        {
            "topic_title": "韩国伯爵.美丽说",
            "topic_url": "sinaweibo://pageinfo?pageid=1008081bb24f3bb3bff159acbba67716311dfd&extparam=%E9%9F%A9%E5%9B%BD%E4%BC%AF%E7%88%B5.%E7%BE%8E%E4%B8%BD%E8%AF%B4"
        }
    ],
    "created_timestamp": 1416389223,
    "bid": "Bx0DlkbNQ",
    "pics": [
        {
            "pid": "005KKCSRtw1emf8ptfm1qj307r0cqq3d",
            "url": "http://ww2.sinaimg.cn/thumb180/005KKCSRtw1emf8ptfm1qj307r0cqq3d.jpg",
            "size": "thumb180",
            "geo": {
                "width": 180,
                "height": 180,
                "croped": false,
                "byte": 26344
            }
        },
        {
            "pid": "005KKCSRtw1emf8pu0zrij306m08taao",
            "url": "http://ww1.sinaimg.cn/thumb180/005KKCSRtw1emf8pu0zrij306m08taao.jpg",
            "size": "thumb180",
            "geo": {
                "width": 180,
                "height": 180,
                "croped": false,
                "byte": 33047
            }
        },
        {
            "pid": "005KKCSRtw1emf8purir7j30a40btaat",
            "url": "http://ww1.sinaimg.cn/thumb180/005KKCSRtw1emf8purir7j30a40btaat.jpg",
            "size": "thumb180",
            "geo": {
                "width": 180,
                "height": 180,
                "croped": false,
                "byte": 38167
            }
        },
        {
            "pid": "005KKCSRtw1emf8pvegrjj30a50drjs2",
            "url": "http://ww3.sinaimg.cn/thumb180/005KKCSRtw1emf8pvegrjj30a50drjs2.jpg",
            "size": "thumb180",
            "geo": {
                "width": 180,
                "height": 180,
                "croped": false,
                "byte": 35374
            }
        }
    ],
    "like_count": 0
}
        :param m_list:
        :return:
        """
        new_list = []
        try:
            for m in m_list:
                m.setdefault('url_struct',[])
                m.setdefault('page_info',{'page_url':''})
                fmt = {}
                fmt['unique_identify'] = 'sina_weibo_'+ m['mid']
                fmt['text_content'] = self.textFilter(m['text'])
                fmt['title'] = self.textFilter(m['text'],False).decode('utf-8')[:80].encode('utf-8')
                fmt['summary'] = m['text']
                fmt['source'] = '新浪微博'
                fmt['type'] = 1 #微博
                fmt['author'] = m['user']['screen_name']
                fmt['link'] = 'http://weibo.com/%s/%s' % (m['user']['id'],m['bid'])
                # if m['url_struct'] and m['url_struct'][0]:
                #     fmt['link'] = m['url_struct'][0]['short_url']
                # else:
                #     fmt['link'] = m['page_info']['page_url']
                #
                fmt['pub_date'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(m['created_timestamp']))
                #额外记录该微博用户的信息
                fmt['json_data'] = {
                    'mid' : m['mid'],
                    'user_id' : m['user']['id'],
                    'user_profile_url':  'http://weibo.com%s' % m['user']['profile_url'],
                    'user_gender' : m['user']['gender'],
                }
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化 新浪微博数据 出错 %s ' % e)
        return new_list




class HexunCrawler(Crawler):
    """
    和讯微博爬虫
    """
    def __init__(self,keyword):
        """
        新浪微博爬虫
        :param keyword:
        :return:
        """
        Crawler.__init__(self)
        if not keyword:
            raise RuntimeError('请提供搜索关键词')
        self.keyword = keyword
        #type = 1 全部（默认）
        #       2 ###标注的
        #       3 原创
        #       4 转载
        self.refer = 'http://t.hexun.com/topic.aspx?type=1&value=%s&pg=%s'
        self.api = u'http://tsearch.tool.hexun.com/weiboJson?%s'
        self.page = 1
        self.count = 20
        self.logger = logger.get('opinion.crawler.HexunCrawler')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
        }

    def read(self,page=None,count=None):
        """
        读取微博内容
        :param page: 页码
        :param count: 每页的微博数量
        :return:
        """
        #如果手动设置了要抓取的页面
        if page is not None:
            self.page = page > 0 and page or 1
        if count is not None:
            self.count = count > 0 and count or 50

        #抓取地址可以翻页,count没用。。
        self.headers['Referer'] = self.refer % (json.dumps(self.keyword).replace('\\','%').replace('"',''),self.page)
        self.nonce = int(time.time() * 1000)
        jsonpCallback = "jQuery17%s_%s" % (re.subn('\D','',('%.16f' % random.random()))[0],self.nonce -3216)

        params = urllib.urlencode({"callback":jsonpCallback,"q":self.keyword,"type":1,"value":"0,1","item":self.count,"pg":self.page,"_":self.nonce})
        url = self.api % params

        #请求数据
        result = self.request(url,useProxy=True,headers=self.headers)
        #如果请求失败
        if result is None:
            self.logger.debug('抓取%s数据失败！' % url)
            return []

        #查看页面可以看到是charset=gb2312，所以需要转换编码
        #然后替换掉jsonp的回调函数jQuery(xxxx)
        try:
            info = json.loads(result.decode('gb2312').replace(jsonpCallback+'(','')[:-1])
        except Exception,e:
            self.logger.error('格式化 和讯微博JSON数据 出错 %s ' % e)
            return []
        #如果数据不正确
        if not info['list']:
            self.logger.debug('%s 返回数据不正确!' % url)
            return []

        #自动进入下一页数据
        self.page += 1
        #对微博的消息内容进行分析
        #return analysis(info['list'],type='hexun')
        return self.format(info['list'])


    def format(self,m_list):
        """
        格式化内容为统一的格式
        其中和讯微博的内容格式：
        {
    "articleId": "42453271",
    "blogName": "25399987",
    "content": "utm/zbTy1OzQwsqxtPrIq9DCzfi5uszl0ekgLSC+rbOj1NrM1LGmxcTFxLm6zu+1xM3409G2vNaqtcCjrLOjuea1xM34wufJzLXqz+DNrLL6xre827jxuPfW1rj30fmjrNXiysfS8s6qz+DNrL/uyr21xLL6xre/ycTcvq25/cHLtuC0zrXE1tDXqqOs1+6687LFsNrJz834teq79bzco6y2+LG+zsTSqr2ytb21xLrZv83T67TztuDK/bXEzfjC57m6zu/N+NW+srvSu9H5o6zT67OnyczWsb3Tus/X96OsutjmwiA8YSBocmVmPSJodHRwOi8vaGV4dW51cmwuY24vMnRSc0giIHRpdGxlPSJodHRwOi8vMjUzOTk5ODcuYmxvZy5oZXh1bi5jb20vOTY3MzUwOTRfZC5odG1sIiB0YXJnZXQ9Il9ibGFuayI+aHR0cDovL2hleHVudXJsLmNuLzJ0UnNIPC9hPg==",
    "forwardFromArticleId": "0",
    "forwardFromContent": "",
    "forwardFromUserId": "0",
    "forwardFromUserName": "",
    "forwardState": "0",
    "fromArticleId": "0",
    "fromUserId": "0",
    "fromUserName": "",
    "linkFlag": "1",
    "photoId": "0",
    "photoState": "0",
    "photoUrl": "",
    "postIp": "10.0.200.151",
    "pubTime": "MjAxNMTqMTHUwjE5yNUgMTU6MTY=",
    "quotePhotoId": "0",
    "quotePhotoUrl": "",
    "quoteStockCode": "",
    "rssTitle": "",
    "rssUrl": "",
    "source": "525",
    "stockFlag": "0",
    "userId": "25399987",
    "userName": "bWFpbDI1OTY5MTg2",
    "value": 0,
    "videoPhotoUrl": "",
    "videoState": "0",
    "videoUrl": "",
    "voteId": "0",
    "voteInfo": "",
    "voteState": "0"
}
        :param m_list:
        :return:
        """
        new_list = []
        try:
            for m in m_list:
                fmt = {}
                fmt['unique_identify'] = 'hexun_weibo_'+ m['articleId']
                content = base64.decodestring(m['content']).decode('gb2312','ignore').encode('utf-8','ignore')
                fmt['title'] = re.subn('<a\shref=.*?</a>','',content)[0].decode('utf-8','ignore')[:80].encode('utf-8','ignore')
                fmt['summary'] = content
                fmt['text_content'] = self.textFilter(content)
                fmt['source'] = '和讯微博'
                fmt['type'] = 1 #微博
                fmt['author'] = base64.decodestring(m['userName']).decode('gb2312','ignore').encode('utf-8','ignore')
                p = re.compile(ur'title="(.*?)"\s?')
                link = re.search(p,content)
                if link :
                    fmt['link'] = link.group(1)
                else:
                    # fmt['link'] = 'http://%s.blog.hexun.com/%s_d.html' % (m['userId'],m['articleId'])
                    fmt['link'] = ''

                t = time.strptime(base64.decodestring(m['pubTime']).decode('gb2312').encode('utf-8'), '%Y年%m月%d日 %H:%M')
                fmt['pub_date'] = time.strftime('%Y-%m-%d %H:%M:%S',t)
                #额外记录该微博用户的信息
                fmt['json_data'] = {
                    'user_id':m['userId'],
                    'user_profile_url': 'http://%s.blog.hexun.com/' % (m['userId']),
                    'article_id':m['articleId'],
                    'blog_name':m['blogName'],
                    'post_ip':m['postIp'],
                }
                new_list.append(fmt)
        except Exception,e:
            self.logger.error('格式化 和讯微博数据 出错 %s ' % e)
        return new_list
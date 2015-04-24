#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
启动脚本
"""
from crawler import Opinion

if __name__ == '__main__':
    #手动触发更新，不然会同时更新

    #
    opinion = Opinion({
        'weibo':[u'美丽说徐易容',u'美丽说投诉',u'美丽说曝光',u'美丽说太差',u'美丽说质量',u'美丽说HIGO',u'美丽说骗',u'美丽说垃圾',u'美丽说坑爹',u'美丽说DESIRE'],
        #'weibo':[],
        'news':[u'美丽说',u'美丽说徐易容',u'美丽说投诉',u'美丽说曝光',u'美丽说太差',u'美丽说质量',u'美丽说HIGO',u'美丽说骗',u'美丽说垃圾',u'美丽说坑爹',u'美丽说DESIR ']
    })
    #opinion.test(-1)
    opinion.get()

    # for m in opinion.get():
    #     print m['title']

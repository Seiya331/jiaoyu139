#!/usr/bin/env python
# coding: utf-8
#__author__ = 'apple'
#2015/04/16
#舆情系统的工具包
import re
import sys

def tool_strip_tag(html):
    str = re.sub(r'</?\w+[^>]*>','',html)
    return str

def tool_trim(html):
    if isinstance(html, basestring):
        content_regex = re.compile(r'\s+')
        html = re.sub(content_regex,' ',html)
        return html
    return ''
def tool_write_file(file_name,file_content):
    f = open(file_name,'w')
    f.write(file_content)
    f.close()
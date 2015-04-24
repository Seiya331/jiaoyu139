#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
日志处理类
"""


import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import logging
import logging.config


config = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','config','logging.conf'))
logging.config.fileConfig(config)

def get(name):
    return logging.getLogger(name)
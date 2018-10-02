#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : appstore
@Time : 2018/4/5 下午5:18
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site :
@File : setting.py
@desc :
"""

COOKIE_SECRET = '91orTzKXQAsaYekL7gEtGlJJFuYh7EQnp2XdTP1o/Vo='
JQUERY_LIB = '/static/js/jquery-latest.js'

DOMAIN = 'hxzwmk.com'

UPLOAD_DIR = '/var/www/ssdb/attachment'

# 用于记录输出到stdout的log信息
MY_APP = 'my_app'

MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 8  # 程序关闭/重启等待时间 秒

CATE_LIST = list()
CATE_DICT_REVERSE = {}
CATE_DICT = {
    u'电视直播': 'tv_play',
    u'视频点播': 'video',
    u'音乐娱乐': 'music',
    u'工具': 'tool',
    u'其他': 'other'
}

for k, v in CATE_DICT.iteritems():
    CATE_LIST.append(k)
    CATE_DICT_REVERSE[v] = k

RECOMMEND_APP_LIST = [
    'com.vcinema.client.tv',
]

root_name = 'root@root.com'
root_secret = 'happy123'
password = 'f162dbe9eaeb42b21019cf4a314964f3'
root_salt = 'i said'

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
@File : common.py
@desc :
"""

from time import time
from urllib import urlencode


def insert_time_to_code(code, times=None):
    """ 把时间戳打散插入到激活码,code 32s """
    if times is None:
        times = str(int(time()))
    tmp_str = []
    index = 0
    for i in range(10):
        index = (i+1)*2
        tmp_str.append(code[i*2:index])
        tmp_str.append(times[i])
    tmp_str.append(code[index:])
    return ''.join(tmp_str)


def remove_time_from_encode(en_code):
    """ 从已加时间戳的字符串移除时间戳 """
    tmp_str = []
    index = 0
    for i in range(10):
        index = i*3
        tmp_str.append(en_code[index:index+2])
    tmp_str.append(en_code[index+3:])
    return ''.join(tmp_str)


def set_big_file_upload_url(arg_dict, url='/bigfile/upload'):
    url += "?" + urlencode(arg_dict)
    return url

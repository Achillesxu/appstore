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
@File : db.py
@desc :
"""


from ssdb import SSDB

# 主业务
db = SSDB(host='127.0.0.1', port=8887, socket_timeout=600)


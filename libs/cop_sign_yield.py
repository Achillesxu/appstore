#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : 7po
@Time : 2017/12/26 下午3:50
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : cop_sign_yield.py
@desc :
"""
import hashlib
import operator

from libs.db import db
import setting


def produce_cop_signature(args):
    return hashlib.md5(reduce(operator.add, args)).hexdigest()


web_jump_sign = produce_cop_signature([str(setting.cop_app_id), setting.cop_app_key])


if __name__ == '__main__':
    # print(hashlib.md5('www.7po.com').hexdigest())
    print web_jump_sign

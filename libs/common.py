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
@File : commons.py
@desc :
"""

import logging
import os
from time import time
from datetime import datetime, timedelta
import re
from hashlib import md5

import jieba
from libs.hzszm import get_szm
from libs.pinyin import get_pinyin


class Property(object):
    """
    Return a property attribute for new-style classes.
    It only implement __get__ method, so you are free to set __dict__ to
    override this property.
    That's the only reason you would like to use it instead of the build-in
    property function.

    将方法封装成一个属性，适用于新风格的类。
    由于只实现了__get__方法，所以你可以自由地设置__dict__，以覆盖对它的访问。
    这也是你采用它，而不使用内建的property函数的唯一原因。
    """

    def __init__(self, fget):
        """
        @type fget: function
        @param fget: the function for getting an attribute value

        用于获取属性的函数
        """
        self.fget = fget
        self.__doc__ = fget.__doc__

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError, 'unreadable attribute'
        return self.fget(obj)


class CachedProperty(Property):
    """
    Return a property attribute for new-style classes.
    It works the same as Property, except caching the calculated property to its __dict__.

    将方法封装成一个属性，适用于新风格的类。
    作用与Property相同，不同之处是会把计算出来的属性缓存到__dict__。
    """

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        fget = self.fget
        if fget is None:
            raise AttributeError, 'unreadable attribute'
        obj.__dict__[fget.__name__] = prop = fget(obj)
        return prop


def size2str(size_byte):
    mb = 1000*1000
    if size_byte >= mb:
        return '%.2f MB' % (float(size_byte)/mb)
    if size_byte >= 1000:
        return '%d KB' % int(size_byte/1000)
    return '%d B' % size_byte


def make_n(mod=10, base=1):
    # return datetime.now().microsecond % mod + base
    return 1


def get_n(n=1):
    if n:
        return n*11
    return 1


def time_tran(t):
    return t[0:4] + '-' + t[4:6] + '-' + t[6:8]


def count_num_fm(num):
    if num < 10000:
        return str(num)
    if num < 100000000:
        return '%.1f万' % (float(num)/10000)
    return '%.1f亿' % (float(num)/100000000)


def mk_dir(my_path):
    if not os.path.exists(my_path):
        try:
            os.makedirs(my_path)
        except:
            logging.error('mkdir false:' + my_path)


def tm2date(timemap):
    return datetime.fromtimestamp(timemap)


def cn_time():
    return datetime.utcnow() + timedelta(hours=+8)


def tm2strb(timemap):
    return datetime.fromtimestamp(timemap).strftime('%Y-%m-%d')


def tm2str2(timemap, fmt='%Y-%m-%d %H:%M'):
    # 2014-04-12 11:12
    return datetime.fromtimestamp(timemap).strftime(fmt)


def tm2str(timemap):
    return datetime.fromtimestamp(timemap).strftime('%Y-%m-%d %H:%M:%S')


def tm2str3(timemap):
    # 04-12
    return datetime.fromtimestamp(timemap).strftime('%m-%d')


def tm2str_xml(timemap):
    # 20140501T125959 年月日T时分秒
    return datetime.fromtimestamp(timemap).strftime('%Y%m%dT%H%M%S')


def get_year_mon_str():
    return datetime.fromtimestamp(int(time())).strftime('%Y%m')


def get_ymd_str():
    return datetime.fromtimestamp(int(time())).strftime('%Y%m%d')


def get_ymd_str2():
    return datetime.fromtimestamp(int(time())).strftime('%Y-%m-%d')


def get_last_7days(n_day):
    ymd_list = []
    for i in range(1, n_day+1):
        dt = datetime.utcnow() + timedelta(days=-i, hours=+8)
        ymd = dt.strftime('%Y%m%d')
        ymd_list.append(ymd)
    return ymd_list


def get_yesterday_ymd():
    dt = datetime.utcnow() + timedelta(days=-1, hours=+8)
    return dt.strftime('%Y%m%d')

email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$", re.IGNORECASE)


def is_email(text):
    if '@' in text:
        # return re.match(r'^[^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$|^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}$', text)
        return email_regex.match(text)
    return False


def is_mobile(text):
    return re.match(r'(13|14|15|18)\d{9}$', text)


def check_username(text):
    """判断用户名的类型，返回user 表对应的查询字段 （name/email/mobile）"""
    if '@' in text and is_email(text):
        return 'email', text
    if re.match(r'^\d{11}$', text) and is_mobile(text):
        return 'mobile', text
    if re.match(r'^[a-zA-Z][a-zA-Z0-9]{3,19}$', text):
        return 'name', text
    return False


def md5_salt(text, salt):
    """ 密码加盐 """
    salt_md5 = md5(text + salt).hexdigest()
    return md5(salt_md5).hexdigest()


def gen_active_code(email, pw):
    pw_md5 = md5(pw).hexdigest()
    email_md5 = md5(email).hexdigest()
    return md5(''.join([pw_md5, email_md5, email, pw])).hexdigest()


def is_char_num(text):
    # m_re = re.compile('^[A-Za-z0-9_ ]+$')
    m_re = re.compile('^[A-Za-z0-9_]+$')
    return m_re.match(text)


def szm_filter_char(text):
    text = text.lower().strip().replace(' ', '').replace(' ', '').replace('：', '').replace('·', '')
    # char_re = re.compile(r"[ \-,\@\'\"\[\]\. · _\+\(\)：∞]")
    char_re = re.compile(r"""[\-,\@\'\"\[\]\._\+\(\)]""")
    return char_re.sub('', text)


cn_re = re.compile(u"[\u4e00-\u9fa5]+")


def cn_filter(text):
    """ 过滤掉中文 """
    return cn_re.sub('', text.decode("utf8"))


def cnnow():
    return datetime.utcnow() + timedelta(hours=+8)


def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp)


def time_from_now(dtime):
    if isinstance(dtime, int):
        dtime = timestamp_to_datetime(dtime)
    # time_diff = datetime.utcnow() - time
    time_diff = cnnow() - dtime
    days = time_diff.days
    if days:
        if days > 730:
            return '%s天前' % (days / 365)
        if days > 365:
            return '1年前'
        if days > 60:
            return '%s月前' % (days / 30)
        if days > 30:
            return '1月前'
        if days > 14:
            return '%s周前' % (days / 7)
        if days > 7:
            return '1周前'
        if days > 1:
            return '%s天前' % days
        return '1天前'
    seconds = time_diff.seconds
    if seconds > 7200:
        return '%s小时前' % (seconds / 3600)
    if seconds > 3600:
        return '1小时前'
    if seconds > 120:
        return '%s分钟前' % (seconds / 60)
    if seconds > 60:
        return '1分钟前'
    if seconds > 1:
        return '%s秒前' % seconds
    return '%s秒前' % seconds


def get_text_fenci(text):
    """"获取输入的分词及分词拼音、首字母"""
    new_obj = {}
    # # 获取首字母和全拼
    if is_char_num(text):
        title_lower = text.lower()
    else:
        title_lower = szm_filter_char(text)
    # print new_obj['name'], title_lower
    jp_qp = get_pinyin(title_lower)
    new_obj['name_qp'] = jp_qp[1]  # 1
    try:
        new_obj['name_szm'] = get_szm(title_lower)
    except:
        new_obj['name_szm'] = jp_qp[0]
        # print 'get name szm error:', title_lower, new_obj['name_szm']
    name_szm1 = szm_filter_char(new_obj['name_szm'])
    new_obj['name_szm'] = name_szm1
    if ',' in new_obj['name_qp']:
        name_szm2 = ''.join([x[0] for x in new_obj['name_qp'].split(',')])
        if name_szm1 != name_szm2:
            new_obj['name_szm'] = ','.join([name_szm1, name_szm2])

    # 分词
    seg_list = jieba.cut_for_search(title_lower)
    fen_ci_list = []
    for x in seg_list:
        tmp = x.strip().replace('[', '').replace(']', '')
        if tmp:
            fen_ci_list.append(tmp)
    # fen_ci = ",".join([x for x in seg_list if x.strip().replace('[', '').replace(']', '')])
    fen_ci = ','.join(list(set(fen_ci_list)))
    fen_ci = fen_ci.strip(',')
    szm_list = []
    qp_list = []
    for ci in fen_ci.split(','):
        if ci:
            try:
                szm_tmp = get_szm(ci)
            except:
                szm_tmp = get_pinyin(ci)[0]
                # print 'get szm_tmp error: ', ci, szm_tmp

            if szm_tmp:
                szm_list.append(szm_tmp)
                # jp_qp = get_pinyin(ci, '_')
                jp_qp = get_pinyin(ci, '')
                qp_list.append(jp_qp[1])
                szm_list.append(jp_qp[0])
    #
    szm_set = set(szm_list)
    szm_set.discard('')
    new_obj['name_fenci_cn'] = fen_ci  # 分词中文  # 3
    new_obj['name_fenci_szm'] = ','.join([x for x in szm_set if x.strip()])  # 分词首字母  # 4
    new_obj['name_fenci_qp'] = ','.join([x for x in qp_list if x.strip()])  # 分词全拼  # 5
    return new_obj


if __name__ == '__main__':
    # tar_text = 'VST全聚合'
    # t_dict = get_text_fenci(tar_text)
    # print tar_text.lower()
    # print t_dict
    print md5_salt('root@root.com' + 'happy123', 'i said')

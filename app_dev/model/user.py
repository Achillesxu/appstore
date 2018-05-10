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
@File : user.py
@desc :
"""

import os
import logging
import ujson as json
from time import time
from hashlib import md5

from libs.db import db
from libs.common import md5_salt, tm2str
from app_dev.lib.common import insert_time_to_code, get_styles

import setting
import app_dev.setting as dev_setting

root_my_app = logging.getLogger(setting.MY_APP)


class UserModel(object):

    @staticmethod
    def get_user_by_email(email):
        if email == setting.root_name:
            return setting.root_name
        else:
            return None

    @staticmethod
    def login_check(email, password):
        encode_pw = md5_salt(email + password, setting.root_salt)
        if encode_pw == setting.password:
            return True
        return False

    @staticmethod
    def clear_old_tmp_appdata(email):
        name = 'dev_user_apps_tmp:%s' % email
        num = db.hsize(name)
        if num:
            objs = db.hscan(name, '', '', num)
            old_time = (int(time()) - 3600*12)*1000000  # 3600*12
            for key in objs:
                if int(key) < old_time:
                    db.hdel(name, key)
                    # 删除上传的静态文件（只删除apk）
                    value = objs[key]
                    obj = json.loads(value)
                    if 'cp' not in obj:  # 防止在自动清除过期数据时误删文件
                        for k in ['apk_path']:
                            v = str(obj.get(k, ''))
                            if v.startswith('static/upload') or v.startswith(setting.UPLOAD_DIR):
                                v2 = v.replace(setting.UPLOAD_DIR + '/', '')
                                try:
                                    os.remove('%s/%s' % (setting.UPLOAD_DIR, v2))
                                except:
                                    pass

    @staticmethod
    def update_apk_info_tmp(email, time_key, apk_obj):
        if not apk_obj:
            return None
        old_time = (int(time()) - 3600*12)*1000000
        if int(time_key) < old_time:
            return None
        name = 'dev_user_apps_tmp:%s' % email
        value = db.hget(name, time_key)
        if value:
            obj = json.loads(value)
            if 'new_captures' in apk_obj:
                new_cap = apk_obj['new_captures']
                if obj.get('new_captures'):
                    old_caps = obj['new_captures'].split(',')
                else:
                    old_caps = []
                if new_cap in old_caps:
                    #return old_caps.index(new_cap) + 1
                    return old_caps
                else:
                    if apk_obj.get('cap_index', None):
                        int_cap_index = int(apk_obj['cap_index'])
                        if int_cap_index < 1:
                            int_cap_index = 1
                        if int_cap_index < len(old_caps):
                            old_caps[int_cap_index - 1] = new_cap
                            new_caps = old_caps
                        else:
                            old_caps.append(new_cap)
                            new_caps = old_caps[-6:]
                    else:
                        old_caps.append(new_cap)
                        new_caps = old_caps[-6:]
                    obj['new_captures'] = ','.join(new_caps)
                    db.hset(name, time_key, json.dumps(obj))
                    #return new_caps.index(new_cap) + 1
                    return new_caps
            else:
                obj.update(apk_obj)
                db.hset(name, time_key, json.dumps(obj))
        else:
            db.hset(name, time_key, json.dumps(apk_obj))
            if 'new_captures' in apk_obj:
                #return 1
                return [apk_obj['new_captures']]
        return True

    @staticmethod
    def del_cap_img_tmp(email, time_key, cap_index):
        old_time = (int(time()) - 3600*12)*1000000
        if int(time_key) < old_time:
            return None
        cap_index = int(cap_index)
        name = 'dev_user_apps_tmp:%s' % email
        value = db.hget(name, time_key)
        if value:
            obj = json.loads(value)
            # if 'c' in obj:
            if 'new_captures' in obj:
                caps = obj['new_captures'].split(',')
                new_caps = caps[:cap_index-1] + caps[cap_index:]
                obj['new_captures'] = ','.join(new_caps)
                db.hset(name, time_key, json.dumps(obj))
                return new_caps
            else:
                return []
        else:
            return []

    @staticmethod
    def get_user_app_info_tmp(email, time_key):
        name = 'dev_user_apps_tmp:%s' % email
        value = db.hget(name, time_key)
        if value:
            return json.loads(value)
        return {}

    @staticmethod
    def add_user_app_info(email, time_key, app_info):
        name = 'dev_user_apps_package:%s' % email
        #
        db.hset(name, app_info['package'], json.dumps(app_info))
        db.zset(name, app_info['package'], app_info['modified'])
        db.hset(app_info['category'][:-1], app_info['package'], '1')

        # del tmp data
        db.hdel('dev_user_apps_tmp:%s' % email, time_key)

    @staticmethod
    def update_user_app_info(package, email, time_key, app_info, not_change_update_time=False):
        name = 'dev_user_apps_package:%s' % email

        value = db.hget(name, package)
        old_app_info = json.loads(value)
        # # 检测有没有变化
        info_changed = 0
        for k in app_info:
            if k != 'time_key':
                if app_info[k] != old_app_info.get(k, None):
                    info_changed += 1
        #
        old_app_info.update(app_info)
        #
        # # if info_changed > 0:  # 不做信息是否更新检测
        if not_change_update_time:
            # 不更新上架时间
            if old_app_info.get('id'):
                # 获取上次上架的时间
                _v = db.get('app_info:%08d' % old_app_info['id'])
                if _v:
                    _obj = json.loads(_v)
                    old_app_info['modified'] = _obj['updatetime']
        else:
            # 更新上架时间
            old_app_info['modified'] = int(time())
        db.hset(name, package, json.dumps(old_app_info))
        db.zset(name, package, old_app_info['modified'])

        #
        # del tmp data
        db.hdel('dev_user_apps_tmp:%s' % email, time_key)

    @staticmethod
    def get_my_apps_info(email, current_page=1, key_start='', score_start='', page_limit=10):
        name = 'dev_user_apps_package:%s' % email
        total = db.hsize(name)
        total_page = total/page_limit
        if total % page_limit:
            total_page += 1
        #
        app_list = []
        if key_start:
            score_start = int(score_start)
            objs = db.zrscan(name, key_start, score_start, '', page_limit)
            key_list = objs.keys()
            if key_list:
                apps = db.hmget(name, *key_list)
                for k in key_list:
                    app_list.append(json.loads(apps[k]))
        else:
            if total:
                objs_all = db.zrscan(name, '', '', '', total)
                index_from = (current_page-1)*page_limit
                index_to = index_from + page_limit
                #
                i = 0
                key_list = []
                for k in objs_all:
                    if index_from <= i < index_to:
                        key_list.append(k)
                    i += 1
                #
                apps = db.hmget(name, *key_list)
                for k in key_list:
                    app_list.append(json.loads(apps[k]))
        return {'total_num': total, 'total_page': total_page, 'apps': app_list}

    @staticmethod
    def get_my_apps_info_by_kw(email, kw):
        kw = kw.encode('unicode_escape')  # 把中文转码，如：把“人” 转为 “\u4eba”
        page_limit = 10
        name = 'dev_user_apps_package:%s' % email
        total = db.hsize(name)
        if total == 0:
            return {'total_num': 0, 'total_page': 0, 'apps': []}
        app_list = []
        app_key_dict = {}
        #
        if total <= page_limit:
            objs_all = db.zrscan(name, '', '', '', total)
            key_list = objs_all.keys()
            apps = db.hmget(name, *key_list)
            for k in key_list:
                value = apps.get(k, '')
                if kw in value:
                    if k not in app_key_dict:
                        app_list.append(json.loads(value))
                        app_key_dict[k] = True
        else:
            key_start = ''
            score_start = ''
            while len(app_list) < page_limit:
                objs = db.zscan(name, key_start, score_start, '', page_limit*3)
                if not objs:
                    break
                key_list = objs.keys()
                apps = db.hmget(name, *key_list)

                for k in key_list:
                    key_start = k
                    score_start = objs[k]
                    #
                    value = apps.get(k, '')
                    if kw in value:
                        if k not in app_key_dict:
                            app_list.append(json.loads(value))
                            app_key_dict[k] = True
                            if len(app_list) >= page_limit:
                                break
        #
        return {'total_num': len(app_list), 'total_page': 1 if len(app_list) else 0, 'apps': app_list}

    @staticmethod
    def del_user_app(email, package):
        name = 'dev_user_apps_package:%s' % email
        value = db.hget(name, package)
        if value:
            obj = json.loads(value)
            try:
                base_dir = setting.UPLOAD_DIR
                # new_captures
                for img in obj['new_captures'].split(','):
                    os.remove('%s/%s' % (base_dir, img))
                # new_logo
                os.remove('%s/%s' % (base_dir, obj['new_logo']))
                # icon
                os.remove('%s/%s' % (base_dir, obj['icon']))
                # apk_path - 全路径
                os.remove(obj['apk_path'])
                db.hdel(obj['category'][:-1], package)
            except Exception:
                pass
        db.hdel(name, package)
        db.zdel(name, package)

    @staticmethod
    def get_user_app_info_for_edit(email, package):
        value = db.hget('dev_user_apps_package:%s' % email, package)
        if value:
            obj = json.loads(value)
            return obj
        return None

    @staticmethod
    def get_category_package_list(category, email=setting.root_name):
        if category:
            return db.hkeys(category, '', '', db.hsize(category))
        else:
            return db.hkeys('dev_user_apps_package:%s' % email, '', '', db.hsize('dev_user_apps_package:%s' % email))

    @staticmethod
    def get_app_package_list(email, p_list):
        res_list = list()
        if p_list:
            r_dict = db.hmget('dev_user_apps_package:%s' % email, *p_list)
            for k, v in r_dict.iteritems():
                d_tmp = dict()
                if v:
                    try:
                        d_app = json.loads(v)
                    except Exception:
                        pass
                    else:
                        d_tmp['name'] = d_app['name']
                        d_tmp['package'] = d_app['package']
                        d_tmp['versioncode'] = d_app['versioncode']
                        d_tmp['versionname'] = d_app['versionname']
                        d_tmp['category'] = d_app['category'][:-1]
                        d_tmp['apk_path'] = 'http://{}/{}'.format(setting.DOMAIN, d_app['apk_path'])
                        d_tmp['icon'] = 'http://{}/{}'.format(setting.DOMAIN, d_app['icon'])
                        d_tmp['logo'] = 'http://{}/{}'.format(setting.DOMAIN, d_app['new_logo'])
                        d_tmp['captures'] = ','.join(['http://{}/{}'.format(setting.DOMAIN, i)
                                                     for i in d_app['new_captures'].split(',')])
                        d_tmp['apk_md5'] = d_app['apk_md5']
                        d_tmp['app_size'] = d_app['appsize']
                        res_list.append(d_tmp)
            return res_list
        else:
            return res_list

    @staticmethod
    def get_app_detail(email, package_name):
        pkg_list = db.hkeys('dev_user_apps_package:%s' % email, '', '', db.hsize('dev_user_apps_package:%s' % email))
        d_tmp = dict()
        if package_name in pkg_list:
            j_app = db.hget('dev_user_apps_package:%s' % email, package_name)
            if j_app:
                try:
                    d_app = json.loads(j_app)
                    d_tmp['name'] = d_app['name']
                    d_tmp['package'] = d_app['package']
                    d_tmp['versioncode'] = d_app['versioncode']
                    d_tmp['versionname'] = d_app['versionname']
                    d_tmp['category'] = d_app['category'][:-1]
                    d_tmp['apk_path'] = 'http://{}/{}'.format(setting.DOMAIN, d_app['apk_path'])
                    d_tmp['icon'] = 'http://{}/{}'.format(setting.DOMAIN, d_app['icon'])
                    d_tmp['logo'] = 'http://{}/{}'.format(setting.DOMAIN, d_app['new_logo'])
                    d_tmp['captures'] = ','.join(['http://{}/{}'.format(setting.DOMAIN, i)
                                                 for i in d_app['new_captures'].split(',')])
                    d_tmp['apk_md5'] = d_app['apk_md5']
                    d_tmp['app_size'] = d_app['appsize']
                except Exception as e:
                    d_tmp['error_code'] = -1
                    d_tmp['error_reason'] = '{}'.format(e)
                    return d_tmp
                else:
                    return d_tmp
            else:
                d_tmp['error_code'] = -1
                d_tmp['error_reason'] = 'cant find this info of {}'.format(package_name)
                return d_tmp
        else:
            d_tmp['error_code'] = -1
            d_tmp['error_reason'] = 'please confirm {}'.format(package_name)
            return d_tmp

    @staticmethod
    def get_user_app_info_for_edit_get(email, package):
        """ 同上，修正旧应用数据的图片显示 """
        value = db.hget('dev_user_apps_package:%s' % email, package)
        if value:
            obj = json.loads(value)
            # fix old data
            # for k in ['new_logo', 'new_captures', 'icon']:
            for k in ['new_logo', 'new_captures', 'icon']:
                if obj[k].startswith('static/upload'):
                    if k == 'new_captures':
                        obj[k] = ','.join(['/%s' % x.strip('/') for x in obj[k].split(',')])
                    else:
                        obj[k] = '/%s' % obj[k].strip('/')
                else:
                    if k == 'new_captures':
                        obj[k] = ','.join(['http://%s/%s' % (setting.DOMAIN, x.strip('/')) for x in obj[k].split(',')])
                    else:
                        obj[k] = 'http://%s/%s' % (setting.DOMAIN, obj[k].strip('/'))
            return obj
        return None

    @staticmethod
    def check_user_package(email, package):
        return db.hexists('dev_user_apps_package:%s' % email, package)

    @staticmethod
    def get_app_info_by_package(package):
        app_id = db.get('app_pack:' + package)
        if app_id:
            value = db.get('app_info:' + app_id)
            if value:
                return json.loads(value)
        return None


if __name__ == '__main__':
    res = UserModel.get_app_package_list('root@root.com', setting.RECOMMEND_APP_LIST)
    print len(res)


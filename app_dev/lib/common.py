#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'weizs'

import os
import logging
import re
import shutil
from time import time
from urllib import urlencode
from commands import getoutput, getstatusoutput
import tempfile
import hashlib
import subprocess

import setting
from libs.common import get_year_mon_str, mk_dir, cn_filter


def md5sum(filename, block_size=65536):
    my_hash = hashlib.md5()
    with open(filename, "r+b") as f:
        for block in iter(lambda: f.read(block_size), ""):
            my_hash.update(block)
    return my_hash.hexdigest()


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
    #url += "?" + urlencode(arg_dict)
    #
    url += "?" + '&'.join(['%s=%s' % (k, v) for k, v in arg_dict.iteritems()])
    return url


def apk_parser(apk_path):
    if not apk_path:
        return None
    app_info = {'sdk_version': 8}  # , 'icon': ''
    text = getoutput("aapt d badging " + apk_path)
    lines = text.splitlines()
    #
    #cn_re = re.compile("[^0-9A-Za-z_\-\.]")
    #
    error = []
    #icon_size = {}
    for line in lines:
        kv = line.split(':')
        if len(kv) >= 2:
            k = kv[0]
            v = ':'.join(kv[1:])  # fixed ':' in value
            if k == 'package':
                m = re.search(r"name='(\S+?)'", v)
                if m:
                    app_info['package'] = m.groups(0)[0]
                else:
                    error.append('获取 包名 出错')
                m = re.search(r"versionCode='(\S+?)'", v)
                if m:
                    app_info['versioncode'] = m.groups(0)[0]
                else:
                    error.append('获取 版本号 出错')
                m = re.search(r"versionName='(.+?)'", v)
                if m:
                    app_info['versionname'] = cn_filter(m.groups(0)[0])
                else:
                    error.append('获取 版本名 出错')
            elif re.match(r'application-label(.*)', k):
                app_info['name'] = v.strip("'")
            elif k == 'sdkVersion':
                app_info['sdk_version'] = v.strip("'")
            #elif re.match(r'application-icon-(\d+)', k):
            #    icon_size[int(k.split('-')[-1])] = v.strip("'")
    # fix parse bug
    # name
    if 'name' not in app_info:
        m = re.findall(r"label='([^']+?)'", text)
        if m:
            app_info['name'] = m[0]
        else:
            m2 = re.findall(r'label="([^"]+?)"', text)
            if m2:
                app_info['name'] = m2[0]
    # 已修改为用户上传icon，不用自动提取icon
    # get max size of icon
    #if icon_size:
    #    max_size = max(icon_size.keys())
    #    icon_path = icon_size[max_size]
    #    tmpd_path = tempfile.mkdtemp()  # 临时文件夹
    #    status, output = getstatusoutput('/usr/bin/unzip %s -d %s' % (apk_path, tmpd_path))
    #    if status == 0:
    #        file_path = 'static/upload/icon_tmp/%s' % get_year_mon_str()
    #        source_file_path = '%s/%s' % (tmpd_path, icon_path)
    #        file_md5 = md5sum(source_file_path)
    #        new_icon_name = '%s.png' % file_md5
    #        icon_url = '%s/%s' % (file_path, new_icon_name)
    #        try:
    #            file_dir = '%s/%s' % (setting.UPLOAD_DIR, file_path)
    #            mk_dir(file_dir)
    #            target_file_ab_path = "%s/%s" % (setting.UPLOAD_DIR, icon_url)
    #            if not os.path.isfile(target_file_ab_path):
    #                shutil.copy(source_file_path, target_file_ab_path)
    #            app_info['icon'] = icon_url
    #        except:
    #            error.append('提取包里icon 失败')
    #    else:
    #        error.append('解压apk 包失败')
    #else:
    #    error.append('分析 icon 路径出错')
    return {'app': app_info, 'error': error}


def get_video_first_frame_img(video_path):
    if not video_path:
        return None
    rsp = {'status': 201}
    video_img_dir = 'static/upload/video_tmp/%s' % get_year_mon_str()
    video_file_name = video_path.split('/')[-1]
    video_img_name = '%s.png' % video_file_name.split('.')[0]
    save_ab_path_img = os.path.join(setting.UPLOAD_DIR, video_img_dir, video_img_name)
    if os.path.isfile(save_ab_path_img):
        rsp['msg'] = '视频截图已存在'
        rsp['status'] = 200
        rsp['video_img'] = '%s/%s' % (video_img_dir, video_img_name)
    else:
        file_dir = '%s/%s' % (setting.UPLOAD_DIR, video_img_dir)
        mk_dir(file_dir)
        out = subprocess.call('ffmpeg -i %s -vframes 1 %s' % (video_path, save_ab_path_img), shell=True)
        if not out:
            # out==0
            rsp['status'] = 200
            rsp['msg'] = '视频截图成功保存'
            rsp['video_img'] = '%s/%s' % (video_img_dir, video_img_name)
        else:
            rsp['msg'] = '视频截图保存失败'
    return rsp


def get_new_upload_static(old_dict, new_dict, force_upload_apk):
    """  输入原来和新的app_info 字典，返回不同的值，供七牛上传 """
    up_file_dict = {}
    # for k in ['apk_md5', 'icon', 'new_logo', 'video', 'video_img', 'new_captures', 'background', 'instruction']:
    for k in ['apk_md5', 'icon', 'new_logo', 'video', 'video_img', 'new_captures']:
        if k == 'new_captures':
            old_caps = old_dict['new_captures'].split(',')
            new_caps = new_dict['new_captures'].split(',')
            old_caps_dict = dict.fromkeys(old_caps, True)
            new_add_caps = []
            for new_cap in new_caps:
                if new_cap not in old_caps_dict:
                    new_add_caps.append(new_cap)
            if new_add_caps:
                up_file_dict['new_captures'] = ','.join(new_add_caps)
        else:
            if new_dict[k]:
                if new_dict[k] != old_dict.get(k, None):
                    if k == 'apk_md5':
                        up_file_dict['apk_url'] = new_dict['apk_url']
                        up_file_dict['slug_url'] = new_dict['slug_url']
                    else:
                        up_file_dict[k] = new_dict[k]
                else:
                    if force_upload_apk:
                        if k == 'apk_md5':
                            up_file_dict['apk_url'] = new_dict['apk_url']
                            up_file_dict['slug_url'] = new_dict['slug_url']
    return up_file_dict


def fix_old_cat_name(tag_list):
    """ 输入tag list 返回一个旧分类名和包含一级分类的新list """
    if isinstance(tag_list, unicode):
        tag_list = tag_list.split(',')
    old_category = ''
    new_tag_list = []
    cat_list = ['video', 'daily', 'games', 'education']
    for tag in tag_list:
        if tag.strip():
            i = 0
            for tags in setting.TAG_DICT:
                if tag in tags:
                    if tags[0] not in new_tag_list:
                        new_tag_list.append(tags[0])
                        if not old_category:
                            old_category = cat_list[i]
                i += 1
            if tag not in new_tag_list:
                new_tag_list.append(tag)
    if not old_category:
        old_category = 'daily'
    if not new_tag_list:
        new_tag_list = ['应用', '生活']
    return {'category': old_category, 'tags': ','.join(new_tag_list)}


def fix_old_style(tag_list):
    """ 输入tag list 返回多个操作方式的 str """
    if isinstance(tag_list, unicode):
        tag_list = tag_list.split(',')
    style_list = []
    for tag in tag_list:
        if tag in setting.STYLE_DICT:
            style_list.append(setting.STYLE_DICT[tag])
    if not style_list:
        style_list = ['1']
    return ','.join(style_list)


def get_styles(work_list):
    style_list = []
    for work in work_list:
        if work in setting.STYLE_DICT:
            style_list.append(setting.STYLE_DICT[work])
    if not style_list:
        style_list = ['1']
    return ','.join(style_list)

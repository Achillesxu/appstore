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

import logging
import os
from hashlib import md5
import ujson as json
from time import time
from StringIO import StringIO
from PIL import Image

import tornado.web

from app_dev.handler.base import BaseHandler
from app_dev.handler.base import authenticated
from app_dev.model.user import UserModel
from libs.common import mk_dir, get_year_mon_str, tm2str, get_text_fenci, is_email
from app_dev.lib.common import insert_time_to_code, remove_time_from_encode, set_big_file_upload_url, \
    apk_parser
import setting


class HomeMainPage(BaseHandler):
    def get(self):
        user = self.current_user
        if user:
            self.redirect('/user/my_apps')
            return
        else:
            self.redirect('/user/login')
            return


class LoginPage(BaseHandler):
    def get(self):
        self.echo('login.html', {
            'title': '登录',
            'check_error': None
        }, layout='_layout.html')

    def post(self):
        self.check_xsrf_cookie()
        email = self.get_argument('email')
        password = self.get_argument('password')

        # 检测正式用户
        user = UserModel.login_check(email, password)
        if user:
            self.set_secure_cookie("email", str(email))
            self.redirect('/user/my_apps')
            return
        self.echo('login.html', {
            'title': '登录',
            'check_error': '用户名或密码不正确'
        }, layout='_layout.html')


class LogoutPage(BaseHandler):
    def get(self):
        # self.clear_all_cookies()
        self.clear_cookie('email')
        self.redirect('/user/login')


class HomePage(BaseHandler):
    def get(self):
        user = self.current_user
        if user:
            self.redirect('/user/my_apps')
            return
        else:
            self.redirect('/user/login')
            return


class MyAppsPage(BaseHandler):
    @authenticated
    def get(self):
        email = self.current_user
        # del app
        act = self.get_argument('act', None)
        if act == 'del':
            package = self.get_argument('package', None, strip=False)
            if package:
                UserModel.del_user_app(email, package)
                self.redirect('/user/my_apps')
                return
        key_start = self.get_argument('key_start', '')
        score_start = self.get_argument('score_start', '')
        page = self.get_argument('page', '1')
        page = int(page)
        kw = self.get_argument('kw', '')
        if kw:
            my_apps_info = UserModel.get_my_apps_info_by_kw(email, kw)
        else:
            my_apps_info = UserModel.get_my_apps_info(email, page, key_start, score_start)

        self.echo('my_apps.html', {
            'title': '我的应用',
            'kw': kw,
            'current_page': page,
            'total_page': my_apps_info['total_page'],
            'total_num': my_apps_info['total_num'],
            'my_apps': my_apps_info['apps'],
        }, layout='_layout.html')


class AddAppPage(BaseHandler):
    @authenticated
    def get(self):
        time_str = ('%.6f' % time()).replace('.', '')
        secure_email = self.get_cookie('email')
        # 删除图片
        act = self.get_argument('act', None)
        if act == 'delcap':
            time_key = self.get_argument('time_str', None)
            cap_index = self.get_argument('cap_index', None)
            rsp = {}
            if time_key and cap_index:
                img_list = UserModel.del_cap_img_tmp(self.current_user, time_key, cap_index)
                rsp['status'] = 200
                rsp['img_len'] = len(img_list)
                if img_list:
                    rsp['img_list'] = ['/' + x for x in img_list]
                else:
                    rsp['img_list'] = img_list
                self.write(json.dumps(rsp))
                return
        #
        arg_apk_dict = {'act': 'add', 'time': time_str, 'code': secure_email, 'next': '/upload/apk'}
        uploader_apk = set_big_file_upload_url(arg_apk_dict)
        #
        # 清空用户的过期数据
        UserModel.clear_old_tmp_appdata(self.current_user)
        self.echo('add_app.html', {
            'title': '添加应用',
            'time_str': time_str,
            'secure_email': secure_email,
            'uploader_apk': uploader_apk,
        }, layout='_layout.html')

    @authenticated
    def post(self):
        time_key = self.get_argument('time_str', None)
        if time_key is None:
            return
        category = self.get_argument('language')
        intro = self.get_argument('intro')
        update_log = self.get_argument('update_log', '')

        app_info = {
            'category': setting.CATE_DICT[category] + '1',
            'email': self.current_user,
            'intro': intro,
            'modified': int(time()),
            'update_log': update_log,
        }
        other_info = UserModel.get_user_app_info_tmp(self.current_user, time_key)
        if other_info:
            app_info.update(other_info)
        # #检测一些必填的信息
        errors = []
        if 'package' not in app_info:
            errors.append('没有上传apk')
        if 'icon' not in app_info:
            errors.append('没有上传应用 icon')
        if 'new_logo' not in app_info:
            errors.append('没有上传推荐位图片')
        if 'new_captures' not in app_info:
            errors.append('没有上传应用截图')
        if not intro:
            errors.append('没有填写应用简介')
        if errors:
            self.write('请解决下列错误<br/>')
            self.write('<br/>'.join(errors))
            return

        UserModel.add_user_app_info(self.current_user, time_key, app_info)
        self.redirect('/user/my_apps')


class EditAppPage(BaseHandler):
    @authenticated
    def get(self):
        email = self.current_user
        time_str = ('%.6f' % time()).replace('.', '')
        package = self.get_argument('package', None, strip=False)  # 版本号多出空格
        app_info = UserModel.get_user_app_info_for_edit_get(email, package)
        if app_info is None:
            self.write('app is None')
            return
        if not app_info.get('update_log', None):
            app_info['update_log'] = ''
        #
        secure_email = self.get_cookie('email')
        #
        arg_apk_dict = {'act': 'edit', 'time': time_str, 'code': secure_email, 'next': '/upload/apk'}
        uploader_apk = set_big_file_upload_url(arg_apk_dict)
        # 清空用户的过期数据
        UserModel.clear_old_tmp_appdata(self.current_user)
        # 把原来的截图cp 过来
        app_info_source = UserModel.get_user_app_info_for_edit(email, package)
        UserModel.update_apk_info_tmp(email, time_str, {
            'new_captures': app_info_source['new_captures'],
            'icon': app_info_source['icon']})
        self.echo('edit_app.html', {
            'title': '编辑应用',
            'app_info': app_info,
            'time_str': time_str,
            'secure_email': secure_email,
            'uploader_apk': uploader_apk,
        }, layout='_layout.html')

    @authenticated
    def post(self):
        email = self.current_user
        time_key = self.get_argument('time_str', None)
        if time_key is None:
            return
        package = self.get_argument('package', None)
        old_app_info = UserModel.get_user_app_info_for_edit(email, package)
        if old_app_info is None:
            self.write('app is None')
            return
        category = self.get_argument('language')
        intro = self.get_argument('intro')
        modified = int(self.get_argument('modified'))
        update_log = self.get_argument('update_log')
        # 在打开修改页面和提交修改之间存在一次修改（最后修改时间不一致）
        # 发生的情况：多人编辑或单人多窗口同时修改一个应用
        if modified != old_app_info['modified']:
            self.write('应用已被修改，请 <a href="/user/edit_app?package=%s">重新载入</a> 后再修改' % package)
            return

        app_info = {
            'category': setting.CATE_DICT[category] + '1',
            'intro': intro,
            'email': self.current_user,
            'update_log': update_log,
            # 'modified': int(time())
        }
        other_info = UserModel.get_user_app_info_tmp(email, time_key)
        if other_info:
            app_info.update(other_info)

        # #检测一些必填的信息
        errors = []
        if not intro:
            errors.append('没有填写应用简介')
        if 'package' in app_info:
            if app_info['package'] != old_app_info['package']:
                errors.append('所上传的apk 包名不同： %s / %s' % (app_info['package'], old_app_info['package']))
        if not app_info.get('icon'):
            errors.append('没有上传icon')
        if errors:
            self.write('请解决下列错误<br/>')
            self.write('<br/>'.join(errors))
            return

        UserModel.update_user_app_info(package, email, time_key, app_info)
        self.redirect('/user/my_apps')


class UploadAPKPage(BaseHandler):
    @authenticated
    def get(self):
        # {'time': '1406542080780915',
        # 'code': 'MTIzQHFxLmNvbQ%3D%3D%7C1406279533%7C87e1c57e9829f3e3ea76da3e76ee78721ae56ab1',
        # 'file_path': '/home/weis/projects/pythoncode/tmp/1406542104179.apk',
        # 'file_md5': '80c67ffa96a12306efac8160a2e6cd2b',
        # 'file_size': '27818192'}
        recived_dict = {k: ''.join(v) for k, v in self.request.arguments.iteritems()}
        if not recived_dict:
            self.write('no data')
            return
        email = self.current_user
        time_key = recived_dict['time']
        apk_info = apk_parser(recived_dict.get('file_path', None))
        status = 200
        apk_obj = apk_info['app'].copy()
        goto_url = ''
        if apk_info['error']:
            msg = '<br/>'.join(apk_info['error'])
            status = 201
        else:
            msg = ''
            apk_obj['apk_path'] = recived_dict['file_path']
            apk_obj['apk_md5'] = recived_dict['file_md5']
            apk_obj['appsize'] = int(recived_dict['file_size'])
            if 'name' not in apk_obj or 'versioncode' not in apk_obj or 'versionname' not in apk_obj and 'package' not in apk_obj:
                # logging.error(apk_obj)
                msg = '上传的apk 包解析错误'
                status = 201
            act = recived_dict['act']
            # 若是添加
            if act == 'add':
                # check exist package # 同一用户不能添加相同包名的apk
                if UserModel.check_user_package(email, apk_obj['package']):
                    msg = '您已添加包名为：%s 的apk，请在我的应用里搜索该包名，点进去直接更新' % apk_obj['package']
                    status = 302
                    goto_url = '/user/edit_app?package=%s' % apk_obj['package']
            elif act == 'edit':
                pass
        apk_obj['time_key'] = time_key
        rsp = {
            'status': status,
            'apk_name': apk_obj.get('name', ''),
            'apk_versioncode': apk_obj.get('versioncode', ''),
            'apk_versionname': apk_obj.get('versionname', ''),
            'apk_package': apk_obj.get('package', ''),
            # 'apk_icon': apk_obj['icon'],
            'msg': msg,
            'goto_url': goto_url
        }
        if status == 200:
            apk_obj['apk_path'] = apk_obj['apk_path'].replace(setting.UPLOAD_DIR + '/', '')
            up_result = UserModel.update_apk_info_tmp(email, time_key, apk_obj)
            if up_result is None:
                rsp['status'] = 201
                rsp['msg'] = '会话已过期，请刷新页面'
                self.write(json.dumps(rsp))
                return

        self.write(json.dumps(rsp))


class UploadIconPage(BaseHandler):
    @authenticated
    def post(self):
        # logging.error('in py icon')
        rsp = {'status': 201, 'msg': 'waiting'}
        time_key = self.get_argument('time', None)
        upload_file = self.request.files.get('upload_file')
        file_md5 = md5(upload_file[0]['body']).hexdigest()
        # 检测图片大小
        im = Image.open(StringIO(upload_file[0]['body']))
        wh = im.size
        if min(wh) < 200:
            rsp['msg'] = '请上传边长至少为200 px 的正方形icon：所上传的是 %d x %d px' % wh
            self.write(json.dumps(rsp))
            return
        save_file_name = "%s.png" % file_md5
        file_path = 'static/upload/icon_tmp/%s' % get_year_mon_str()
        ab_path = os.path.join(setting.UPLOAD_DIR, file_path, save_file_name)
        # check exist
        if os.path.isfile(ab_path):
            rsp['msg'] = '文件已存在'
        else:
            file_dir = '%s/%s' % (setting.UPLOAD_DIR, file_path)
            # try to mkdir
            mk_dir(file_dir)
            with open(ab_path, 'wb') as tmp:
                tmp.write(upload_file[0]['body'])
            rsp['msg'] = '成功上传'

        icon_url = '%s/%s' % (file_path, save_file_name)
        # email = self.get_argument('email')
        email = self.current_user
        up_rezult = UserModel.update_apk_info_tmp(email, time_key, {'icon': icon_url})
        if up_rezult is None:
            rsp['msg'] = '会话已过期，请刷新页面'
            self.write(json.dumps(rsp))
            return
        rsp['status'] = 200
        rsp['icon_url'] = '/' + icon_url
        self.write(json.dumps(rsp))


class UploadCoverPage(BaseHandler):
    @authenticated
    def post(self):
        # logging.error('in py cover')
        rsp = {'status': 201, 'msg': 'waiting'}
        time_key = self.get_argument('time', None)
        upload_file = self.request.files.get('upload_file')
        file_md5 = md5(upload_file[0]['body']).hexdigest()
        save_file_name = "%s.png" % file_md5
        file_path = 'static/upload/cover_tmp/%s' % get_year_mon_str()
        ab_path = os.path.join(setting.UPLOAD_DIR, file_path, save_file_name)
        # check exist
        if os.path.isfile(ab_path):
            rsp['msg'] = '文件已存在'
        else:
            file_dir = '%s/%s' % (setting.UPLOAD_DIR, file_path)
            # try to mkdir
            mk_dir(file_dir)
            with open(ab_path, 'wb') as tmp:
                tmp.write(upload_file[0]['body'])
            rsp['msg'] = '成功上传'

        logo_url = '%s/%s' % (file_path, save_file_name)
        # email = self.get_argument('email')
        email = self.current_user
        up_rezult = UserModel.update_apk_info_tmp(email, time_key, {'new_logo': logo_url})
        if up_rezult is None:
            rsp['msg'] = '会话已过期，请刷新页面'
            self.write(json.dumps(rsp))
            return
        rsp['status'] = 200
        rsp['logo_url'] = '/' + logo_url
        self.write(json.dumps(rsp))


class UploadCapturePage(BaseHandler):
    @authenticated
    def post(self):
        # logging.error('in py cap')
        rsp = {'status': 201, 'msg': 'waiting'}
        time_key = self.get_argument('time', None)
        cap_index = self.get_argument('cap_index', None)
        upload_file = self.request.files.get('upload_file')
        file_md5 = md5(upload_file[0]['body']).hexdigest()
        save_file_name = "%s.png" % file_md5
        file_path = 'static/upload/capture_tmp/%s' % get_year_mon_str()
        ab_path = os.path.join(setting.UPLOAD_DIR, file_path, save_file_name)
        # check exist
        if os.path.isfile(ab_path):
            rsp['msg'] = '文件已存在'
        else:
            file_dir = '%s/%s' % (setting.UPLOAD_DIR, file_path)
            # try to mkdir
            mk_dir(file_dir)
            with open(ab_path, 'wb') as tmp:
                tmp.write(upload_file[0]['body'])
            rsp['msg'] = '成功上传'

        img_url = '%s/%s' % (file_path, save_file_name)
        img_list = UserModel.update_apk_info_tmp(self.current_user, time_key,
                                                 {'new_captures': img_url, 'cap_index': cap_index})
        if img_list is None:
            rsp['msg'] = '会话已过期，请刷新页面'
            self.write(json.dumps(rsp))
            return
        rsp['status'] = 200
        rsp['img_len'] = len(img_list)
        if img_list:
            rsp['img_list'] = ['/' + x for x in img_list]
        else:
            rsp['img_list'] = img_list
        rsp['img_url'] = '/' + img_url
        self.write(json.dumps(rsp))


class UploadImgFile(BaseHandler):
    # 用lua 脚本处理上传的文件的接口，icon,cover,capture, maybe be with background and instruction(removerd by achilles_xushy)
    @authenticated
    def get(self):
        rsp = {'status': 201, 'msg': 'waiting'}

        act = self.get_argument('act', None)
        time_key = self.get_argument('time', None)
        file_url = self.get_argument('file_url', None)

        cap_index = self.get_argument('cap_index', None)

        if act and time_key and file_url:
            pass
        else:
            rsp['msg'] = 'missing arg'
            self.write(json.dumps(rsp))
            return

        ab_path = os.path.join(setting.UPLOAD_DIR, file_url)
        # check exist
        if not os.path.isfile(ab_path):
            rsp['msg'] = 'file not exist'
            self.write(json.dumps(rsp))
            return

        email = self.current_user

        up_dict = {}
        if act == 'icon':
            rsp['icon_url'] = '/' + file_url
            up_dict = {'icon': file_url}
        elif act == 'cover':
            rsp['logo_url'] = '/' + file_url
            up_dict = {'new_logo': file_url}
        elif act == 'capture':
            up_dict = {'new_captures': file_url, 'cap_index': cap_index}

        up_rezult = UserModel.update_apk_info_tmp(email, time_key, up_dict)
        if up_rezult is None:
            rsp['msg'] = '会话已过期，请刷新页面'
            self.write(json.dumps(rsp))
            return
        rsp['status'] = 200

        if act == 'capture':
            img_list = up_rezult
            rsp['img_len'] = len(img_list)
            if img_list:
                rsp['img_list'] = ['/' + x for x in img_list]
            else:
                rsp['img_list'] = img_list
            rsp['img_url'] = '/' + file_url

        self.write(json.dumps(rsp))


class RecommendAppList(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        res_dict = dict()
        res_dict['apps'] = UserModel.get_app_package_list(setting.root_name, setting.RECOMMEND_APP_LIST)
        res_dict['num'] = len(res_dict['apps'])
        self.write(json.dumps(res_dict))


class AppDetail(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        package_name = self.get_argument('package', '')
        d_res = UserModel.get_app_detail(setting.root_name, package_name)
        self.write(json.dumps(d_res))


class AppUpdate(tornado.web.RequestHandler):
    def get(self):
        """
        {
            'package': 'versioncode',
            'package': 'versioncode',
            'package': 'versioncode',
        }
        :return:
        """
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        package_json = self.get_argument('package_json', '')
        ret_dict = dict()
        try:
            p_dict = json.loads(package_json)
            p_list = [i for i in p_dict.iterkeys()]
            res_list = UserModel.get_app_package_list(setting.root_name, p_list)
            for j in res_list:
                if int(p_dict[j['package']]) < int(j['versioncode']):
                    ret_dict[j['package']] = j
        except Exception as e:
            self.write(json.dumps(ret_dict.update({'error_reason': e, 'error_code': -1})))
        else:
            self.write(json.dumps(ret_dict))


class AppCategoryList(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        category = self.get_argument('category', '')
        res_dict = dict()
        if category not in [i for i in setting.CATE_DICT_REVERSE.iterkeys()]:
            category = ''
        p_list = UserModel.get_category_package_list(category)
        res_dict['apps'] = UserModel.get_app_package_list(setting.root_name, p_list)
        res_dict['num'] = len(res_dict['apps'])
        self.write(json.dumps(res_dict))


class PageNotFoundHandler(BaseHandler):
    def get(self):
        self.set_status(404)
        self.write('404, no this page!!!')

    post = get


if __name__ == '__main__':
    pass

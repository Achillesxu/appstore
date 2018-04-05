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
@File : base.py
@desc :
"""
import logging
import os
import ujson as json
from time import time

import functools
from urllib import urlencode, unquote
import urlparse

import tornado.web
import tenjin
from tenjin.html import *
from tenjin.helpers import *

from app_dev.model.user import UserModel

import setting
import app_dev.setting as dev_setting
from libs.common import size2str, tm2str2, time_from_now, tm2str

engine = tenjin.Engine(
    path=[os.path.join('app_dev', 'templates', theme) for theme in ['admin', 'default']],
    cache=tenjin.MemoryCacheStorage(),
    preprocess=True
)


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)

    def get_login_url(self):
        return '/user/login'

    def get_current_user(self):
        email = self.get_secure_cookie("email")
        # fixed no cookie value in User-Agent for Shockwave Flash and for lua upload
        if email is None:
            secure_email = self.get_argument('secure_email', None)
            if secure_email:
                pass
            else:
                secure_code = self.get_argument('code', None)
                if secure_code:
                    secure_email = unquote(secure_code)
                else:
                    secure_email = ''
            email = tornado.web.decode_signed_value(self.application.settings["cookie_secret"], 'email', secure_email)

        return UserModel.get_user_by_email(email) if email else None

    def render(self, template, context=None, globals=None, layout=False):
        if context is None:
            context = {}
        args = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            xsrf_form_html=self.xsrf_form_html,
            xsrf_token=self.xsrf_token,
            secure_cookie_email=self.get_secure_cookie("email"),
            cur_times=int(time())
        )

        context.update(args)
        return engine.render(template, context, globals, layout)

    def echo(self, template, context=None, globals=None, layout=False):
        self.write(self.render(template, context, globals, layout))


def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        current_user = self.current_user
        if not current_user:
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # jQuery 等库会附带这个头
                self.set_header('Content-Type', 'application/json; charset=UTF-8')
                self.write(json.dumps({'success': False, 'msg': u'您的会话已过期，请重新登录！'}))
                return
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise tornado.web.HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper

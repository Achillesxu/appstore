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
@File : urls.py
@desc :
"""
import app_dev.handler.user


handler = [
    (r"/", app_dev.handler.user.HomeMainPage),
    (r"/user/login", app_dev.handler.user.LoginPage),
    (r"/user/logout", app_dev.handler.user.LogoutPage),
    (r"/user/home", app_dev.handler.user.HomePage),
    (r"/user/my_apps", app_dev.handler.user.MyAppsPage),
    (r"/user/add_app", app_dev.handler.user.AddAppPage),
    (r"/user/edit_app", app_dev.handler.user.EditAppPage),
    #
    (r"/upload/apk", app_dev.handler.user.UploadAPKPage),
    #
    (r"/upload/icon", app_dev.handler.user.UploadIconPage),
    (r"/upload/cover", app_dev.handler.user.UploadCoverPage),
    (r"/upload/capture", app_dev.handler.user.UploadCapturePage),

    (r"/upload/imgfile", app_dev.handler.user.UploadImgFile),
    #
    (r"/recommend/apps_list", app_dev.handler.user.RecommendAppList),
    (r"/app/detail/get", app_dev.handler.user.AppDetail),
    (r"/app/update/get", app_dev.handler.user.AppUpdate),
    (r"/app/list/get", app_dev.handler.user.AppCategoryList),

    (r'.*', app_dev.handler.user.PageNotFoundHandler)
]

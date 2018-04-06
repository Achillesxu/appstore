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
@File : application.py
@desc : server main entrance
"""

import sys
import logging
import time
import signal
import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.log

import setting
reload(sys)
sys.setdefaultencoding('utf-8')

__author__ = 'weizs'

# achilles_xushy-2016-11-10 添加日志的格式化信息, 将需要记录的信息记录在stdout，在supervisor的控制下，也被卸载文件里面，
# 所以去supervisor的配置文件里面查找stdout文件的目录
logging.basicConfig(level=logging.INFO,
                    format='%(name)s-%(levelname)s－%(asctime)s-%(module)s-%(filename)s-[line:%(lineno)d]-%(message)s')


root_myapp = logging.getLogger(setting.MY_APP)
root_myapp.propagate = False
stdout_info = logging.StreamHandler(stream=sys.stdout)
stdout_formatter = logging.Formatter(
    '%(name)s-%(levelname)s－%(asctime)s-%(module)s-%(filename)s-[line:%(lineno)d]-%(message)s')
stdout_info.setFormatter(stdout_formatter)
root_myapp.addHandler(stdout_info)
root_myapp.setLevel(logging.INFO)


tornado.log.LogFormatter(fmt='[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s',
                         datefmt='%y-%m-%d %H:%M:%S')


class Application(tornado.web.Application):
    def __init__(self):
        from app_dev.urls import handler as dev_handler

        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret=setting.COOKIE_SECRET,
            autoescape=None,
            # debug=True,
        )

        handlers = [
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            # (r".*", handler.topic.NotFound),
        ]
        handlers.extend(dev_handler)

        tornado.web.Application.__init__(self, handlers, **settings)


def sig_handler(sig, frame):
    logging.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)


def shutdown():
    logging.info('Stopping http server')
    server.stop()

    logging.info('Will shutdown in %s seconds ...', setting.MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + setting.MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            logging.info('Shutdown')
    stop_loop()


def main():
    try:
        port = int(sys.argv[1])
    except:
        # port = 8888
        port = 15009

    global server

    server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
    server.listen(port)

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    tornado.ioloop.IOLoop.instance().start()

    logging.info("Exit...")


if __name__ == "__main__":
    main()

# coding: utf-8
import os
import sys
from common.paths import server_path
sys.path.append(os.path.join(server_path, 'packages'))

# init logging
from common.logging import logger_init
logger_init()

import time
import signal
import logging
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.wsgi
from tornado.options import options, define
from src.db_models import models
from urls.url import routes

define("debug", default=1, help="debug mode: 1 to open, 2 to test env, other to production")
define("port", default=9000, help="port, default: 9000")

settings = {
    "xsrf_cookies": False,
    "debug": bool(options.debug),
    "static_path": os.path.join(os.path.dirname(__file__), "statics"),
    "template_path": os.path.join(os.path.dirname(__file__), 'templates'),
}


class Application(tornado.web.Application):
    def __init__(self):
        global settings
        super().__init__(routes, **settings)


def sig_handler(sig, frame):
    """信号处理函数
    """
    logging.info('\nReceived interrupt signal: %s' % sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)


def shutdown():
    """进程关闭处理
    """
    logging.warning('Stopping http server, please wait...')
    # 停止接受Client连接
    application.stop()

    io_loop = tornado.ioloop.IOLoop.instance()
    # 设置最长等待强制结束时间
    deadline = time.time() + 5

    def stop_loop():
        now = time.time()
        if now < deadline:
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
    stop_loop()


if __name__ == "__main__":
    # 等待supervisor发送进程结束信号
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    # initialize database
    models.init_db_data()

    # parse command arguments
    tornado.options.parse_command_line()

    # create application object
    app = Application()

    application = tornado.httpserver.HTTPServer(app, xheaders=True)

    if options.debug == 1:
        debug_str = "in debug mode"
        application.listen(options.port)
    elif options.debug == 2:
        logging.warning("run test success, exiting...")
        sys.exit(0)
    else:
        debug_str = "in production mode"
        application.bind(options.port)
        application.start(3)

    logging.info("running {0} @ {1}...".format(debug_str, options.port))
    tornado.ioloop.IOLoop.instance().start()

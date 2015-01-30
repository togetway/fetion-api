# -*- coding:utf-8 -*-
#!/usr/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options
import tornado.web

import log

class CEntryHTTPApplication(tornado.web.Application):
    def log_request(self, handler):
        if handler.get_status() < 400:
            log_method = log.http.info
        elif handler.get_status() < 500:
            log_method = log.http.warning
        else:
            log_method = log.http.error

        request_time = 1000.0 * handler.request.request_time()

        log_method('%d %s %.2fms', handler.get_status(),
                    handler._request_summary(), request_time)

class CHTTPServer(object):
    def __init__(self, ip, port, logconf):
        #配置日志
        self._configure(ip, port, logconf)

        self._application = CEntryHTTPApplication()
        self._http_server = tornado.httpserver.HTTPServer(self._application)
        self._http_server.listen(options.port)

    def _configure(self, ip, port, logconf):
        define("port", default = port, help = "run on the given port",
                type = int)
        define("address", default = ip or "127.0.0.1", help = "run in localhost",
                type = str)

        tornado.options.parse_command_line(('-logging=True',
                                            '-log_file_prefix=%s'%logconf,
                                            '-log_to_stderr=False',))

    def add_handler(self, handlers):
        self._application.add_handlers(r"", handlers)

    def start(self, callback, interval):
        self._scheduler = tornado.ioloop.PeriodicCallback(callback, interval)
        self._scheduler.start()

        tornado.ioloop.IOLoop.instance().start()

    def stop(self):
        self._http_server.stop()
        tornado.ioloop.IOLoop.instance().stop()

if __name__ == '__main__':
    svr = CHTTPServer(conf/dbconf.ini)
    svr.start()

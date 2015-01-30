# -*- coding:utf-8 -*-
#!/usr/bin/env python

import time
import db
import log
import httpserver
import control

class CWebServer(object):
    def __init__(self, conf):
        #数据库连接
        self._db = db.database.CDataBase(conf.db.db_conf)

        #HTTP服务器
        self._http = httpserver.CHTTPServer(conf.http.ip, int(conf.http.port),
                                            conf.http_log.log_conf)
        self._init_http_server()


    def _init_http_server(self):
        handlers = [
                    (r'/fetion', control.fetion.Fetion, dict(db = self._db)), #飞信接口
                    (r'/email', control.email.Email, dict(db = self._db)), #邮件通知接口
                    (r'/filterip', control.manager.FilterIP, dict(db = self._db)), #单服飞信操作
                    (r'/fetionstatus', control.manager.FetionStatus, dict(db = self._db)), #飞信状态
                    (r'/fetionmanager', control.manager.FetionManager, dict(db = self._db)), #总开关管理
                    ]

        self._http.add_handler(handlers)

    #释放cpu
    def _do_idle(self):
        time.sleep(0.001)

    def start(self):
        #1分钟发送一次心跳
        self._http.start(self._ping, 60000)

    def _ping(self):
        #发送数据库心跳
        self._db.ping()

    def shutdown(self):
        #停止HTTP服务器
        self._http.stop()

        #停止DB
        self._db.close()

if __name__ == "__main__":
    web = CWebServer()
    web.start()

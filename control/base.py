# -*- coding:utf-8 -*-
#!/usr/bin/env python


import time, os
import hashlib

import tornado.web

import log
import constant
import commands

class BaseHandler(tornado.web.RequestHandler):

    def initialize(self, db):
        self._db = db

    def check_user(self):
        para = self.get_argument('para').strip()    #时间
        flag = self.get_argument('flag').strip()    #认证信息

        value = hashlib.md5()
        value.update('%s%s'%(para, constant.KEY))
        new_flag = value.hexdigest()
        if new_flag == flag:
            #log.game.info("[Fetion][_check_user] succ para:%s, flag:%s"% (para, flag))
            return True
        else:
            log.game.info("[Fetion][_check_user] error para:%s, flag:%s"% (para, flag))
            return False

    def check_ip(self):
        ip = self.request.remote_ip #访问IP
        #判断IP
        if ip in constant.FETION_MANAGER_IP:
            return True
        else:
            log.game.info("[Fetion][_check_user] error ip: %s" % (ip))
            return False


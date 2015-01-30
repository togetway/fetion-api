# -*- coding:utf-8 -*-
#!/usr/bin/env python

import time, os
import hashlib

import tornado.web

import log
import constant
import commands

from base import BaseHandler


class Fetion(BaseHandler):
    def get(self):
        self.post()

    def post(self):
        user = self.get_argument('user').strip(',') #发送号码列表
        msg = self.get_argument('msg').strip()   #发送信息
        ip = self.request.remote_ip #访问IP

        #认证密码
        if not self.check_user():
            self.write('check key error.')
            return

        #发送的内容
        msg = '%s(%s)' %(msg,ip)

        #判断接口是否开启
        if self._check_filter(ip):
            if self._send_fetion(user, msg):
                status = 'OK'
            else:
                status = 'NO'
        else:
            status = 'Close'

        #保存发送日志
        self._save_log(user, msg, ip, status)

        self._return('status:%s\n' % status)


    def _return(self, result):
        self.write(result)


    def _check_user(self, para, flag):
        value = hashlib.md5()
        value.update('%s%s'%(para, constant.KEY))
        new_flag = value.hexdigest()
        if new_flag == flag:
            log.game.info("[Fetion][_check_user] succ para:%s, flag:%s"% (para, flag))
            return True
        else:
            log.game.info("[Fetion][_check_user] error para:%s, flag:%s"% (para, flag))
            return False

    def _send_fetion(self, user, msg, num = 1):
        shell_order = "%s --mobile=%s --pwd=%s --to=%s --msg-type=1 --msg-utf8='%s' --exit-on-verifycode=1 > /dev/null" % (constant.FETION_EXE, constant.FETION_USER, constant.FETION_PWD,
        user, msg)
        shell_order = shell_order.encode('utf-8')
        re = os.system(shell_order)
        if re != 0:
            if num > 3:
                log.game.error("[Fetion] [_send_fetion] error user:%s, msg:%s" % (user, msg))
                return False
            log.game.info("[Fetion] [_send_fetion] try num=%d" % (num))
            tornado.ioloop.IOLoop.instance().add_timeout(time.time() + 4, lambda: self._send_fetion(user, msg, num + 1))
        log.game.info("[Fetion][_send_fetion] succ user:%s, msg:%s"% (user, msg))
        return True

    def _save_log(self,user, msg, ip, status):
        msg = msg.encode('utf-8')
        sql = u"insert into fetion_log(user, msg, ip, status, stime) values(%s, %s, %s, %s, now())"
        self._db.update_sql(sql, (user, msg, ip, status))

    def _check_filter(self, ip):
        if os.path.isfile("/tmp/close_fetion"):
            log.game.info("[Fetion] [_check_filter] Master switch is close. ip:%s" % ip)
            return False
        sql = "select * from filter_ip where ip = %s and stime >= NOW();"
        rows = self._db.select_sql(sql, (ip))
        if rows:
            return False
        return True

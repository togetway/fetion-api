# -*- coding:utf-8 -*-
#!/usr/bin/env python

import time, os
import hashlib

import tornado.web

import log
import constant
import commands

from base import BaseHandler



class Email(BaseHandler):
    def get(self):
        self.post()

    def post(self):
        user = self.get_argument('user').strip(',') #发送邮箱列表
        msg = self.get_argument('msg').strip()   #发送信息
        ip = self.request.remote_ip #访问IP

        

        #认证密码
        if not self.check_user():
            self._return('check key error.')
            return

        msg = '%s(%s)' %(msg,ip) #发送的内容


         #判断接口是否开启
        if self._check_filter(ip):
            if self._send_mail(user, msg):
                status = 'OK'
            else:
                status = 'NO'
        else:
            status = 'Close'

        self._return('status:%s\n' % status)


    def _return(self, result):
        self.write(result)


    def _check_user(self, para, flag):
        value = hashlib.md5()
        value.update('%s%s'%(para, constant.KEY))
        new_flag = value.hexdigest()
        if new_flag == flag:
            log.game.info("[Email][_check_user] succ para:%s, flag:%s"% (para, flag))
            return True
        else:
            log.game.info("[Email][_check_user] error para:%s, flag:%s"% (para, flag))
            return False

    def _send_mail(self, user, msg, num = 1):
        shell_order = "/bin/echo '%s' | /bin/mail -s '%s' %s >> /dev/null" % (msg, msg, user)
        shell_order = shell_order.encode('gb2312')
        re = os.system(shell_order)
        if re != 0:
            if num > 3:
                log.game.error("[Email] [_send_mail] error user:%s, msg:%s" % (user, msg))
                return False
            log.game.info("[Email] [_send_mail] try num=%d" % (num))
            tornado.ioloop.IOLoop.instance().add_timeout(time.time() + 4, lambda: self._send_mail(user, msg, num + 1))
        log.game.info("[Email][_send_mail] succ user:%s, msg:%s"% (user, msg))
        return True

    def _check_filter(self, ip):
        if os.path.isfile("/tmp/close_fetion"):
            log.game.info("[Email] [_check_filter] Master switch is close. ip:%s" % ip)
            return False
        sql = "select * from filter_ip where ip = %s and stime >= NOW();"
        rows = self._db.select_sql(sql, (ip))
        if rows:
            return False
        return True




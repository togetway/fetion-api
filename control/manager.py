# -*- coding:utf-8 -*-
#!/usr/bin/env python

#飞信管理

import time, os
import hashlib
import json
import tornado.web

import log
import constant
import commands
from base import BaseHandler



class FetionManager(BaseHandler):
    def post(self):
        action = self.get_argument('action').strip()    #操作

        #认证密码
        if not self.check_user():
            ret = {'status': 0, 'result': u'key认证出错'}
            self.write(json.dumps(ret))
            return

        #判断IP
        if not self.check_ip():
            ret = {'status': 0, 'result': u'访问IP限制'}
            self.write(json.dumps(ret))
            return


        if action == 'close_all':
            commands.getstatusoutput('touch /tmp/close_fetion')
            if os.path.isfile("/tmp/close_fetion"):
                ret = {'status': 1, 'result': u'关闭飞信总接口成功'}
                
            else:
                ret = {'status': 0, 'result': u'关闭飞信总接口失败'}
            self.write(json.dumps(ret))
            return
        elif action == 'open_all':
            commands.getstatusoutput('rm -f /tmp/close_fetion')
            if not os.path.isfile("/tmp/close_fetion"):
                ret = {'status': 1, 'result': u'成功开启飞信总接口'}
            else:
                ret = {'status': 0, 'result': u'开启飞信总接口失败'}
            self.write(json.dumps(ret))
            return
        elif action == 'clearip':
            re = self._clear_filter_ip()
            if re:
                ret = {'status': 1, 'result': u'成功清空限制列表'}
            else:
                ret = {'status': 1, 'result': u'失败'}
            self.write(json.dumps(ret))
            return
        else:
            ret = {'status': 0, 'result': 'action is error'}
            self.write(json.dumps(ret))
            return

    #清空飞信限制列表
    def _clear_filter_ip(self):
        sql = 'delete from filter_ip'
        rows = self._db.update_sql(sql, ())
        return rows


class FilterIP(BaseHandler):
    def post(self):
        action = self.get_argument('action').strip()
        serverip = self.get_argument('serverip').strip()
        hours = self.get_argument('hours', 1)


        #认证密码
        if not self.check_user():
            ret = {'status': 0, 'result': u'key认证出错'}
            self.write(json.dumps(ret))
            return

        #判断IP
        if not self.check_ip():
            ret = {'status': 0, 'result': u'访问IP限制'}
            self.write(json.dumps(ret))
            return

        if action == 'add':
            self._add_filter(serverip, hours)
            log.game.info("[Fetion] [add_filter_ip] ip: %s, hours: %s" % (serverip, hours))
            ret = {'status': 1, 'result': u'限制IP%s飞信%s小时内不发送' % (serverip, hours)}
            self.write(json.dumps(ret))
            return

        elif action == 'del':
            self._del_filter(serverip)
            log.game.info("[Fetion] [del_filter_ip] ip: %s" % serverip)
            ret = {'status': 1, 'result': u'删除IP%s飞信发送限制' % serverip}
            self.write(json.dumps(ret))
            return
        else:
            ret = {'status': 0, 'result': 'action is error'}
            self.write(json.dumps(ret))
            return



    def _add_filter(self, ip, hours):
        sql = 'insert into filter_ip(ip,stime) values(%s, date_add(NOW(), interval %s hour))'
        rows = self._db.update_sql(sql, (ip, hours))
        return rows

    def _del_filter(self, ip):
        sql = 'delete from filter_ip where ip = %s'
        rows = self._db.update_sql(sql, (ip))
        return rows



class FetionStatus(BaseHandler):
    def post(self):
        #认证密码
        if not self.check_user():
            ret = {'status': 0, 'result': u'key认证出错'}
            self.write(json.dumps(ret))
            return

        #判断IP
        if not self.check_ip():
            ret = {'status': 0, 'result': u'访问IP限制'}
            self.write(json.dumps(ret))
            return


        master_swith = self._master_swith()
        filter_list = self._filter_list()

        result = {'master_swith': master_swith, 'filter_list': filter_list}
        ret = {'status': 1, 'result': result}
        self.write(json.dumps(ret))
        return

    #总开关状态
    def _master_swith(self):
        if os.path.isfile("/tmp/close_fetion"):
            return 'closed'
        else:
            return 'opening'

    #限制ip列表
    def _filter_list(self):
        sql = 'select ip, DATE_FORMAT(stime,"%%Y-%%m-%%d %%H:%%I:%%S") as stime from filter_ip where stime > NOW();'
        rows = self._db.select_sql(sql, ())
        return rows
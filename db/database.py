#!/usr/bin/env python
# -*- coding=utf-8 -*-

import ConfigParser

import MySQLdb
from MySQLdb import*

import log

class MySQLException:
    pass

class CDataBase(object):
    def __init__(self, conf):
        self._paser_conf(conf)
        self._connect_db()

    #读取ini获得数据库配置
    def _paser_conf(self, conf):
        config = ConfigParser.ConfigParser()
        config.readfp(open(conf))

        self._host = config.get('db', 'host')
        self._user = config.get('db', 'user')
        self._pwd = config.get('db', 'passwd')
        self._database = config.get('db', 'db')
        try:
            self._port = int(config.get('db', 'port'))
        except:
            self._port = 3306

    def _connect_db(self):
        try:
            self._conn = Connection(self._host, self._user, self._pwd,
                                    self._database, self._port,
                                    cursorclass = cursors.DictCursor)
        except MySQLdb.Error, e:
            log.game.error('[connect_db]failed.error:%s'%str(e))
            return

        self._cursor = self._conn.cursor()
        self._cursor.execute('set autocommit=1')
        self._cursor.execute('set names utf8')

    def __del__(self):
        self._cursor.close()
        self._conn.close()

    def update_sql(self, sql, param):
        '''执行insert、update、delete语句'''
        ret = self._cursor.execute(sql, param)
        return ret

    def exec_many_sql(self, sql, param):
        self._cursor.executemany(sql, param)
        return self._cursor.fetchall()

    def select_sql(self, sql, param):
        '''执行select语句'''
        self._cursor.execute(sql, param)
        if self._cursor.rowcount == 0:
            return ()

        return self._cursor.fetchall()
        #return self._convert_to_name()

    def _convert_to_name(self):
        records = self._cursor.fetchall()
        fields = self._get_fields()

        results = []
        for record in records:
            rec = {}
            for i in xrange(len(fields)):
                rec[fields[i]]=record[i]

            results.append(rec)

        return tuple(results)

    def _get_fields(self):
        """map indices to fieldnames"""
        if not self._cursor.description:
            return {}

        results = {}
        column = 0

        for des in self._cursor.description:
            fieldname = des[0]
            results[column] = fieldname
            column = column + 1

        return results

    def ping(self):
        try:
            _ret = self._conn.ping()
        except Exception, e:
            _ret = e

        if _ret is None:
            return True

        ## reconnect
        self.close()
        return self._connect_db()

    def close(self):
        if self._conn != None:
            self._conn.close()

        self._conn = None
        self._cursor = None

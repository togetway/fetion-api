# -*- coding:utf-8 -*-

import logging

def shutdown():
    logging.shutdown()

def game_log():
    return logging.getLogger('game')

def http_log():
    return logging.getLogger('http')

def init_logging(conf):
    import logging.config
    logging.config.fileConfig(conf)
    global game, http
    game = game_log()
    http = http_log()

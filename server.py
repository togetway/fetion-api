# -*- coding:utf-8 -*-

import os, sys
import optparse
import logging

import log
import configure

def main(conf):
    print 'server starting, please wait.'
    conf = configure.make_conf(conf)

    #初始化日志
    log.init_logging(conf.log.log_conf)

    #初始化web服务器
    import webserver
    web = webserver.CWebServer(conf)

    def shutdown(signum, frame):
        # shutdown
        web.shutdown()
        log.shutdown()

        print 'server is going down now.'
        import sys
        sys.exit()

    # register signal(SIGINT) handler
    import signal
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGQUIT, shutdown)
    signal.signal(signal.SIGABRT, shutdown)

    print 'server started!'
    # finally, start game!
    web.start()


if __name__ == '__main__':
    import sys
    port = int(sys.argv[1])

    main('conf/conf.ini', port)

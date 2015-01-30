# -*- coding:utf-8 -*-

reload_mod = ['fetion', 'email', 'manager']

for name in reload_mod:
    mod = __import__(name, globals(), locals())
    reload(mod)

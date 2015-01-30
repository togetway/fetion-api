#! /usr/bin/env python
# -*- coding=utf-8 -*-

from UserDict import DictMixin

class OrderDict(DictMixin):
    def __init__(self):
        self._keys = []
        self._data = {}

    def __setitem__(self, key, value):
        if key not in self._data:
            self._keys.append(key)
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]

    def __delitem__(self, key):
        del self._data[key]
        self._keys.remove(key)

    def keys(self):
        return self._keys

    def first(self):
        if self._keys:
            return self._keys[0]

    def insert(self, key, value):
        if key not in self._data:
            self._keys.insert(0, key)

        self._data[key] = value

    def copy(self):
        copyDict = OrderDict()
        copyDict._data = self._data.copy()
        copyDict._keys = self._keys[:]
        return copyDict

if __name__ == '__main__':
    a = OrderDict()
    a[1] = 2
    a[3] = 4
    a[2] = 6

    a.insert(4, 6)
    
    for i in a:
        print i
    
    b = {}
    b[1] = 2
    b[3] = 4
    b[2] = 6
    
    for i in b:
        print i
    
    

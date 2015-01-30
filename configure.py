# -*- coding:utf-8 -*-

def make_conf(ini):
    '''This function use for mapping an INI file to a object'''
    class DataObject(object):pass
    obj = DataObject()
    import ConfigParser
    parser = ConfigParser.ConfigParser()
    parser.read(ini)
    for sect in parser.sections():
        o = DataObject()
        for opt in parser.options(sect):
            setattr(o, opt, parser.get(sect, opt))
        setattr(obj, sect, o)
    return obj

def make_iter_conf(ini):
    '''This function use for mapping an INI file to a object'''
    class DataObject(object):pass

    class IterDataObject(object):
        def __init__(self):
            self._sections = []

        def __iter__(self):
            for sec in self._sections:
                yield sec

        def set_sections(self, sect, o):
            setattr(self, sect, o)

            self._sections.append(sect)

    obj = IterDataObject()
    import ConfigParser
    parser = ConfigParser.ConfigParser()
    parser.read(ini)
    for sect in parser.sections():
        o = DataObject()
        for opt in parser.options(sect):
            setattr(o, opt, parser.get(sect, opt))
        obj.set_sections(sect, o)
    return obj

if __name__ == '__main__':
    import sys
    ini = sys.argv[1]
##    obj = make_conf(ini)
##    print obj.__dict__['[network'].port

    obj = make_iter_conf(ini)
    for i in obj:
        print i
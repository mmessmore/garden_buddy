#!/usr/bin/env python

DEBUG = True

import rrdtool

RRDPATH = './soil.rrd'

def update(moisture, temperature):
    ret = rrdtool.update(RRDPATH, "N:{0}:{1}".format(moisture, temperature))
    if ret:
        if DEBUG:
            print rrdtoo.error()
        return False
    return True

#!/usr/bin/env python

import sys
import rrdtool
import time
sys.path.append("./lib")
import rrd


ret = rrdtool.create(rrd.RRDPATH, "--step", "300", "--start", str(int(time.time())),
    "DS:moisture:GAUGE:600:U:U",
    "DS:temperature:GAUGE:600:U:U",
    "RRA:AVERAGE:0.5:1:600",
    "RRA:AVERAGE:0.5:6:700",
    "RRA:AVERAGE:0.5:24:775",
    "RRA:AVERAGE:0.5:288:797",
    "RRA:MAX:0.5:1:600",
    "RRA:MAX:0.5:6:700",
    "RRA:MAX:0.5:24:775",
    "RRA:MAX:0.5:444:797")

if ret:
    print rrdtool.error()
    sys.exit(1)

print "Yay!"
print "RRD Path:{0}".format(rrd.RRDPATH)

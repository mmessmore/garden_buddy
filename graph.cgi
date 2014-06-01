#!/usr/bin/env python

import sys
import os
import cgi

import rrdtool
import tempfile
sys.path.append("./lib")
import rrd

(fd, image_file) = tempfile.mkstemp(suffix=".png", prefix="buddy", dir="/tmp")
os.close(fd)

form = cgi.FieldStorage()
start = "-1d"
if "start" in form:
    start = form.getfirst("start")

ret = rrdtool.graph( image_file, "--start", start,
 "DEF:moist={}:moisture:AVERAGE".format(rrd.RRDPATH),
 "DEF:temp={}:temperature:AVERAGE".format(rrd.RRDPATH),
 "LINE1:moist#00FF00:Moisture %",
 "LINE2:temp#0000FF:Temperature(C)\\r",
 "COMMENT:\\n",
 "GPRINT:moist:AVERAGE:Avg Moisture\: %6.2lf %S%%",
 "COMMENT:  ",
 "GPRINT:moist:MAX:Max Moisture\: %6.2lf %S%%\\r",
 "GPRINT:temp:AVERAGE:Avg Temperature\: %6.2lf %SC",
 "COMMENT: ",
 "GPRINT:temp:MAX:Max Temperature\: %6.2lf %SC\\r")

print "Content-Type: image/png"
print

sys.stdout.write(file(image_file, 'rb').read())

os.unlink(image_file)

sys.exit(0)

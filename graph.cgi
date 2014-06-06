#!/usr/bin/env python

import sys
import os
import cgi

import rrdtool
import tempfile

sys.path.append("./lib")
import config

RRD_PATH = "soil.rrd"

(fd, image_file) = tempfile.mkstemp(suffix=".png", prefix="buddy", dir="/tmp")
os.close(fd)

form = cgi.FieldStorage()
start = "-1d"
if "start" in form:
    start = form.getfirst("start")

colors = [ "#000000", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF",
    "#FF00FF", "#C0C0C0", "#336699", "#6699CC", "#606060"]



conf = config.Config()
lineno = 1
sensors = conf.sensors.keys()
sensors.sort()

args = [image_file, "--start", start]
for sensor in sensors:
    args.append("DEF:{}={}:{}:AVERAGE".format(sensor + "_line", RRD_PATH, sensor))
    args.append("LINE{}:{}{}:{}".format(
        lineno, sensor + "_line", colors[lineno], conf.sensors[sensor]['title']))
    lineno += 1

ret = rrdtool.graph(*args)
 
print "Content-Type: image/png"
print

sys.stdout.write(file(image_file, 'rb').read())

os.unlink(image_file)

sys.exit(0)

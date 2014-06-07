#!/usr/bin/env python

import sys
import os
import cgi

import rrdtool
import tempfile

sys.path.append("./lib")
import config

RRD_PATH = "soil.rrd"

def get_sensors(form, conf):
    # all sensors when none specified
    if not "graph" in form:
        return conf.sensors.keys()
    name = form.getfirst("graph")
    # all the sensors if the spec is bogus
    if not name in conf.graphs.keys():
        return conf.sensors.keys()

    sensors = []
    
    for sensor in conf.graphs[name]["sensors"]:
        if sensor in conf.sensors.keys():
            sensors.append(sensor)
    return sensors

def main():
    (fd, image_file) = tempfile.mkstemp(suffix=".png", prefix="buddy", 
            dir="/tmp")
    os.close(fd)

    form = cgi.FieldStorage()
    start = "-1d"
    if "start" in form:
        start = form.getfirst("start")

    colors = [ "#000000", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", 
            "#00FFFF", "#FF00FF", "#C0C0C0", "#336699", "#6699CC", "#606060"]
    conf = config.Config()
    lineno = 1
    args = [image_file, "--start", start]

    sensors = get_sensors(form, conf)

    for sensor in sensors:
        args.append("DEF:{}={}:{}:AVERAGE".format(sensor + "_line", 
            RRD_PATH, sensor))
        args.append("LINE{}:{}{}:{}".format(
            lineno, sensor + "_line", colors[lineno], 
            conf.sensors[sensor]['title']))
        lineno += 1

    rrdtool.graph(*args)
     
    print "Content-Type: image/png"
    print

    sys.stdout.write(file(image_file, 'rb').read())

    os.unlink(image_file)

    sys.exit(0)

if __name__ == '__main__':
    main()

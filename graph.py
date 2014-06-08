#!/usr/bin/env python

import sys
import os
from flask import Flask, make_response, render_template
import rrdtool
import tempfile
sys.path.append("./lib")
import config

app = Flask(__name__)

app.debug = True


conf = config.Config()

@app.route('/')
def front():
    return render_template('index.html', graphs=conf.graphs)

def get_sensors(name, conf):
    # all the sensors if the spec is bogus
    if not name in conf.graphs.keys():
        return conf.sensors.keys()
    sensors = []
    for sensor in conf.graphs[name]["sensors"]:
        if sensor in conf.sensors.keys():
            sensors.append(sensor)
    return sensors

@app.route('/graph/<graph>')
def graph(graph):
    RRD_PATH = "soil.rrd"
    start = "now-1d"
    (fd, image_file) = tempfile.mkstemp(suffix=".png", prefix="buddy",
            dir="/tmp")
    os.close(fd)

    colors = [ "#000000", "#FF0000", "#00FF00", "#0000FF", "#FFFF00",
            "#00FFFF", "#FF00FF", "#C0C0C0", "#336699", "#6699CC", "#606060"]
    conf = config.Config()
    lineno = 1
    args = [image_file, "--start", start]

    sensors = get_sensors(graph, conf)

    for sensor in sensors:
        args.append("DEF:{}={}:{}:AVERAGE".format(sensor + "_line",
            RRD_PATH, sensor))
        args.append("LINE{}:{}{}:{}".format(
            lineno, sensor + "_line", colors[lineno],
            conf.sensors[sensor]['title']))
        lineno += 1

    rrdtool.graph(*args)

    resp = make_response(open(image_file, 'rb').read())
    resp.content_type = "image/png"

    os.unlink(image_file)
    return resp

if __name__ == '__main__':
    port = 8080
    if os.getuid() == 0:
        port = 80
    app.run(host='0.0.0.0', port=port)

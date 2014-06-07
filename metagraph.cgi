#!/usr/bin/env python

import sys
import os
import cgi

sys.path.append("./lib")
import config

def head():
    print """ContentType: text/html

<html>
<head><title>GardenBuddy</title></head>
<body>
<h1>GardenBuddy</h1>
"""

def foot():
    print """
</body>
</html>
"""

def main():
    form = cgi.FieldStorage()
    start = ""
    if "start" in form:
        start = "&start={}".format(form.getfirst("start"))

    head()
    conf = config.Config()

    for graph in conf.graphs.keys():
        print "<h2>{}</h2>".format(conf.graphs[graph]['title'])
        print '<img src="/cgi-bin/graph.cgi?graph={}{}"/>'.format(graph, start)

    foot()
    
if __name__ == '__main__':
    main()

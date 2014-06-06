#!/usr/bin/env python

DEBUG = True

import rrdtool
import logging

RRDPATH = './soil.rrd'

class RRD:
    def __init__(self, path, config):
        self.path = path
        self.config = config
        self.logger = logging.getLogger(__name__)


    def init_rrd(self):
        if os.path.exists(self.path):
            self.logger.info("RRD file (%s) Exists", self.path)
            return True
        self.logger.info("RRD file (%s) doesn't exist.  Creating new.", self.path)

        create_args = [self.path, "--step", "300", "--start", str(int(time.time()))]

        sk = conf.sensors.keys()
        sk.sort()
        for sensor in sk:
            create_args.append("DS:{}:GAUGE:600:U:U".format(sensor))

        create_args.extend(["RRA:AVERAGE:0.5:1:600", "RRA:AVERAGE:0.5:6:700",
            "RRA:AVERAGE:0.5:24:775", "RRA:AVERAGE:0.5:288:797",
            "RRA:MAX:0.5:1:600", "RRA:MAX:0.5:6:700", "RRA:MAX:0.5:24:775",
            "RRA:MAX:0.5:444:797"])

        # Not being able to create a new RRD is fatal
        if rrdtool.create(*create_args):
            self.logger.critical("Could not create new RRD File %s", self.path)
            self.logger.critical(rrdtool.error())
            sys.exit(1)

        return True

    def update(self, *args):
        update_str = "N:"
        for arg in args:
            update_str = "{}:{}".format(update_str, arg)
        self.logger.debug("Updating RRD with %s", update_str)
        # Not being able to update is a warning
        if rrdtool.update(self.path, update_str):
            self.logger.warning("Failed to update RRD %s", self.path)
            self.logger.warning(rrdtool.error())
            return False
        return True

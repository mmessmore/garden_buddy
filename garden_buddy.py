#!/usr/bin/sudo python
"""
Garden Buddy

Like a monitoring system for your garden.
https://github.com/mmessmore/garden_buddy
"""
import time
import sys
import signal
import argparse
import logging

sys.path.append("./lib")
import analog_bb as analog
import temperature
import rrd
import config
import weather

def cleanup(signum, frame):
    """Signal handler to exit nicely"""
    logger = logging.getLogger(__name__)
    logger.debug("Caught signal: %s, frame: %s", signum, frame)
    sys.exit(0)

def getopts():
    """Parse command line arguments

    Returns:
        namespace with options
    """
    description = 'Log garden sensor data to RRD'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-D', '--debug',
            dest='debug',
            action='store_true',
            help="Run in debug mode (overrides -l, -o)")
    parser.add_argument('-l', '--log-level',
            dest='loglevel',
            choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
            default='WARNING',
            help="Set log level")
    parser.add_argument('-o', '--logfile',
            action='store',
            dest='logfile',
            default='-',
            help="Set log file")
    parser.add_argument('-r', '--rrdfile',
            action='store',
            dest='rrdfile',
            default='./soil.rrd',
            help="Set RRD file")
    parser.add_argument('-n', '--no-write',
            dest='no',
            action='store_true',
            help="Skip writing to RRD")
    parser.add_argument('-s', '--interval',
            dest='interval',
            action='store',
            type=int,
            default=300,
            help="Sleep Interval")
    opts = parser.parse_args()

    logging_format = '%(asctime)s %(levelname)s:%(message)s'
    if opts.debug:
        logging.basicConfig(format=logging_format, level=logging.DEBUG)
        return opts

    numeric_level = getattr(logging, opts.loglevel, None)
    logging.basicConfig(format=logging_format, level=numeric_level)
    if opts.logfile != "-":
        handle = logging.handlers.WatchedFileHandler(opts.logfile)
        logger = logging.getLogger(__name__)
        logger.addHandler(handle)

    return opts

def main():
    """ You know.  Actually do stuff """

    # Set up signal handlers for nice exit
    signal.signal(signal.SIGTERM, cleanup)
    signal.signal(signal.SIGINT, cleanup)

    logger = logging.getLogger(__name__)
    logger.debug("Parsing command line options")
    opts = getopts()
    logger.debug("Parsing config file")
    conf = config.Config()
    logger.debug("Setting up RRD")
    myrrd = rrd.RRD(opts.rrdpath, conf)

    while True:
        logger.debug("Polling")
        values = []

        # sort to ensure order
        sensors = conf.sensors.keys()
        sensors.sort()
        for sensor in sensors:
            if conf.sensors[sensor]['type'] == "analog":
                value = analog.poll(conf.sensors[sensor]['id'])
            elif conf.sensors[sensor]['type'] == "w1":
                value = temperature.poll(conf.sensors[sensor]['id'])
            elif conf.sensors[sensor]['type'] == "noaa":
                value = weather.poll(conf.sensors[sensor]['id'])

            logger.info("%s => %d", conf.sensors[sensor]['title'], value)
            values.append(value)

        if not opts.no:
            myrrd.update(*values)

        logger.debug("Sleep for %d seconds...", opts.interval)
        time.sleep(opts.interval)

    # We should never get here, but just in case
    logger.warning("Somehow broke out of the main loop")
    analog.teardown()

if __name__ == '__main__':
    main()

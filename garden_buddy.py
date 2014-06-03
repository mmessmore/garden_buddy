#!/usr/bin/sudo python
import time
import os
import sys
import signal
import argparse
import logging

sys.path.append("./lib")
#import analog
import analog_bb as analog
import temperature
import rrd


def cleanup(signum, frame):
    sys.exit(0)

def getopts():
    description='Log garden sensor data to RRD'
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
        fh = logging.handlers.WatchedFileHandler(opts.logfile)
        logger = logging.getLogger(__name__)
        logger.addHandler(fh)

    return opts

def main():

    opts = getopts()
    logger = logging.getLogger(__name__)

    signal.signal(signal.SIGTERM, cleanup)
    signal.signal(signal.SIGINT, cleanup)


    while True:
        # read the analog pins
        moisture_value = analog.poll(channel=0)
        pot_value = analog.poll(channel=2)

        # poll the thermometer
        temperature_value = temperature.poll()

        logger.info("moisture_value:%s", moisture_value)
        logger.info("pot_value:%s", pot_value)
        logger.info("temperature_value:%s", temperature_value)

        if not opts.no:
            rrd.update(moisture_value, temperature_value)

        time.sleep(opts.interval)

    # We should never get here, but just in case
    moisture.teardown()

if __name__ == '__main__':
    main()

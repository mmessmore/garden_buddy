#!/usr/bin/sudo python
import time
import os
import sys
sys.path.append("./lib")
import moisture
import temperature
import rrd

import signal

DEBUG=True

def cleanup(signum, frame):
    sys.exit(0)

def main():

    signal.signal(signal.SIGTERM, cleanup)
    signal.signal(signal.SIGINT, cleanup)


    while True:
        # read the analog pin
        moisture_value = moisture.poll()

        # poll the thermometer
        temperature_value = temperature.poll()

        if DEBUG:
            print "time:", time.strftime("%c")
            print "moisture_value:", moisture_value
            print "temperature_value:", temperature_value
            print "------------------------------------"

        rrd.update(moisture_value, temperature_value)

        # hang out and do nothing for 5 secs
        time.sleep(300)

    # We should never get here, but just in case
    moisture.teardown()

if __name__ == '__main__':
    main()

#!/usr/bin/env python
import os
import glob

DEBUG=False


devices = glob.glob('/sys/bus/w1/devices/[0-9][0-9]-[0-9]*/w1_slave')
def poll():
    device = devices[0]
    if DEBUG:
        print device
    f = open(device)
    dump = f.read()
    f.close()

    tempstr = dump.split("\n")[1].split(" ")[9]
    temperature = float(tempstr[2:])
    # Put the decimal point in the right place
    return temperature / 1000

if __name__ == '__main__':
    print poll()


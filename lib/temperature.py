#!/usr/bin/env python
import os
import logging

def poll(id):
    logger = logging.getLogger(__name__)
    device = "/sys/bus/w1/devices/{}/w1_slave".format(id)
    logger.debug("1w device:%s", device)
    try:
        f = open(device)
        dump = f.read()
        f.close()
    except:
        logger.warning("Failed to read device %s", device)
        return 0

    tempstr = dump.split("\n")[1].split(" ")[9]
    temperature = float(tempstr[2:])
    # Put the decimal point in the right place
    return temperature / 1000

if __name__ == '__main__':
    import glob
    device = glob.glob("/sys/bus/w1/devices/[0-9]*/w1_slave")[0]
    id=device.split('/')[5]
    print id
    print poll(id)


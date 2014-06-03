#!/usr/bin/env python
import sys
import atexit
import logging
import spidev

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def poll(channel):
    logger = logging.getLogger(__name__)
    if ((channel > 7) or (channel < 0)):
        return -1
    r = spi.xfer2([1,(8+channel)<<4,0])
    value = ((r[1]&3) << 8) + r[2]
    logger.debug("Channel %s returned %d", channel, value)
    return value

def main():
    """Main function for testing"""
    logging.basicConfig(level=logging.DEBUG)
    channel = 0
    if len(sys.argv) == 2:
        channel = int(sys.argv[1])
    print "{} = {}".format(channel, poll(channel))

spi = spidev.SpiDev()
spi.open(0,0)

if __name__ == '__main__':
    main()

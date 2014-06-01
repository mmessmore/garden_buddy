#!/usr/bin/env python
import sys
import atexit
import logging
import RPi.GPIO as GPIO

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPI_CLK = 18
SPI_MISO = 23
SPI_MOSI = 24
SPI_CS = 25


def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    """read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)"""
    logger = logging.getLogger(__name__)
    logger.debug("Reading value from Analog Channel %s", adcnum)

    if ((adcnum > 7) or (adcnum < 0)):
        logger.error("Invalid Analog Channel")
        return -1

    GPIO.output(cspin, True)
    GPIO.output(clockpin, False)  # start clock low
    GPIO.output(cspin, False)     # bring CS low

    commandout = adcnum
    commandout |= 0x18  # start bit + single-ended bit
    commandout <<= 3    # we only need to send 5 bits here
    for i in range(5):
        if (commandout & 0x80):
            GPIO.output(mosipin, True)
        else:
            GPIO.output(mosipin, False)
            commandout <<= 1
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)

    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1
        if (GPIO.input(misopin)):
            adcout |= 0x1

    GPIO.output(cspin, True)

    adcout >>= 1       # first bit is 'null' so drop it
    return adcout

def setup():
    """ Initial GPIO setup"""
    logger = logging.getLogger(__name__)
    logger.debug("Setting up GPIO")
    GPIO.setmode(GPIO.BCM)

    # set up the SPI interface pins
    GPIO.setup(SPI_MOSI, GPIO.OUT)
    GPIO.setup(SPI_MISO, GPIO.IN)
    GPIO.setup(SPI_CLK, GPIO.OUT)
    GPIO.setup(SPI_CS, GPIO.OUT)

    atexit.register(teardown, -1, None)

def teardown(signum, frame):
    """Signal handler"""
    logger = logging.getLogger(__name__)
    logger.debug("Cleaning up GPIO for exit")
    GPIO.cleanup()
    if signum > 0:
        sys.exit(0)

def poll(channel=0):
    logger = logging.getLogger(__name__)
    value = readadc(channel, SPI_CLK, SPI_MOSI, SPI_MISO, SPI_CS)
    logger.debug("Channel %s returned %d", channel, value)
    return value

# Set up our GPIO fun
setup()

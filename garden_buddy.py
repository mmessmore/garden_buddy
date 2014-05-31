#!/usr/bin/sudo python
import time
import os
import sys
import signal
import RPi.GPIO as GPIO

DEBUG = 1

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPI_CLK = 18
SPI_MISO = 23
SPI_MOSI = 24
SPI_CS = 25

def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    """read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)"""
    if ((adcnum > 7) or (adcnum < 0)):
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
    GPIO.setmode(GPIO.BCM)

    # set up the SPI interface pins
    GPIO.setup(SPI_MOSI, GPIO.OUT)
    GPIO.setup(SPI_MISO, GPIO.IN)
    GPIO.setup(SPI_CLK, GPIO.OUT)
    GPIO.setup(SPI_CS, GPIO.OUT)

    signal.signal(signal.SIGTERM, teardown)
    signal.signal(signal.SIGINT, teardown)

def teardown(signum, frame):
    """Signal handler, args are ignored"""
    GPIO.cleanup()
    sys.exit(0)


def main():
    # Set up our GPIO fun
    setup()

    # Moisture sensor connected to adc #0
    moisture_adc = 0;

    last_value = 0 # To track the delta b/w readings
    tolerance = 5

    while True:
        moisture_value_changed = False

        # read the analog pin
        moisture_value = readadc(moisture_adc, SPI_CLK, SPI_MOSI, SPI_MISO, SPI_CS)
        # how much has it changed since the last read?
        moisture_delta = abs(moisture_value - last_value)
        if ( moisture_delta > tolerance ):
            moisture_value_changed = True

        if DEBUG:
            print "time:", time.strftime("%c")
            print "moisture_value:", moisture_value
            print "moisture_delta:", moisture_delta
            print "last_value:", last_value
            print "moisture_value_changed:", moisture_value_changed
            print "------------------------------------"

        last_value = moisture_value

        # hang out and do nothing for 5 secs
        time.sleep(1)

    # We should never get here, but just in case
    teardown()

if __name__ == '__main__':
    main()

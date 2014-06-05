# Garden Buddy

Garden buddy is a little program to run a sensor array off a Raspberry
Pi to track a garden.

Basically it takes data from sensors connected to a the Pi (currently,
moisture, temp, and light) and stuffs the values into an RRD.  It can
also poll environmental data from NOAA via pywapi to graph along with it.

Currently I really only support Dallas 1-Wire thermometers and analog
stuff hooked up via a MCP3008.  I have tried the in-kernel SPI driver,
but found banging bits to be more effective.  I may add support for
I2C-based stuff later, but I may not.

## My hardware
- http://www.adafruit.com/products/856
- http://www.adafruit.com/products/381
- Cheap moisture sensor (ebay search for "moisture sensor")
- Light sensor I got with a Phidgets set I bought a long time ago. (Part number 1127, they don't seem to offer it anytime)

## Prereqs
- Raspbian
- python-pywapi - The Python Weather API for NOAA Data
- python-rrdtool - The python interface to RRD
- Dallas 1-wire drivers loaded for temperature sensing (w1-gpio, w1_therm)

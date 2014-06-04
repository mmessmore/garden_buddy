#!/usr/bin/env python

import sys
import logging
import pywapi
import datetime
import time
import email.utils

logger = logging.getLogger(__name__)

class Weather:
    def __init__(self, station):
        self.station = station
        self.timestamp = datetime.datetime(1970, 1, 1)
        self.timeout = datetime.timedelta(minutes=60)
        self.poll()

    def poll(self):
        if (datetime.datetime.now() - self.timestamp ) < self.timeout:
            return True
        logger.debug("Fetching Weather from %s", self.station)
        self.weather = pywapi.get_weather_from_noaa(self.station)
        self.timestamp = datetime.datetime.fromtimestamp(int(time.mktime(
                    email.utils.parsedate(
                        self.weather['observation_time_rfc822']))))
        return True

    def temperature(self):
        self.poll()
        return self.weather['temp_c']

    def humidity(self):
        self.poll()
        return self.weather['relative_humidity']

    def wind(self):
        self.poll()
        return self.weather['wind_mph']

    def pressure(self):
        self.poll()
        return self.weather['pressure_mb']

    def dewpoint(self):
        self.poll()
        return self.weather['dewpoint_c']

if __name__ == '__main__':
    w = Weather('KMEM')
    print "temp:", w.temperature()
    print "humidity:", w.humidity()
    print "wind:", w.wind()
    print "pressure:", w.pressure()
    print "dewpoint:", w.dewpoint()


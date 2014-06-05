#!/usr/bin/env python
"""
This is a dumb wrapper around pywapi just for NOAA, since I don't care about
weather.dumb and their stupid made up winter storm names.

For long running processes it keeps you in the sweet spot in terms of polling.
"""

import sys
import logging
import pywapi
import datetime
import time
import email.utils

logger = logging.getLogger(__name__)

class Weather:
    """ Simple abstration for NOAA.
    Args:
        station: NOAA Station ID
    """
    def __init__(self, station):
        self.station = station
        self.timestamp = datetime.datetime(1970, 1, 1)
        self.timeout = datetime.timedelta(minutes=60)
        self.poll()

    def poll(self):
        """Refetch weather data if needed (based on time)"""
        if (datetime.datetime.now() - self.timestamp ) < self.timeout:
            return True
        logger.debug("Fetching Weather from %s", self.station)
        self.weather = pywapi.get_weather_from_noaa(self.station)
        self.timestamp = datetime.datetime.fromtimestamp(int(time.mktime(
                    email.utils.parsedate(
                        self.weather['observation_time_rfc822']))))
        return True

    def temperature(self):
        """Get current temperature in C

        Returns:
            The temperature in degrees Celcius
        """
        self.poll()
        return self.weather['temp_c']

    def humidity(self):
        """Get current relative humidity

        Returns:
            The humidity in numbers
        """
        self.poll()
        return self.weather['relative_humidity']

    def wind(self):
        """Get current windspeed in MPH

        Returns:
            The wind speed in Miles/Hour
        """
        self.poll()
        return self.weather['wind_mph']

    def pressure(self):
        """Get current pressure in mb

        Returns:
            The pressure in Milibars
        """
        self.poll()
        return self.weather['pressure_mb']

    def dewpoint(self):
        """Get current dewpoint in C

        Returns:
            The dewpoint in degrees Celcius
        """
        self.poll()
        return self.weather['dewpoint_c']

if __name__ == '__main__':
    w = Weather('KMEM')
    print "temp:", w.temperature()
    print "humidity:", w.humidity()
    print "wind:", w.wind()
    print "pressure:", w.pressure()
    print "dewpoint:", w.dewpoint()

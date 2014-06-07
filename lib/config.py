#!/usr/bin/env python

import sys
import os
import ConfigParser

class ConfigError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value


class Config:
    def __init__(self):
        conffiles = [
                '/etc/gb.conf',
                '/usr/local/etc/gb.conf',
                os.path.expanduser('~/.gb.conf'),
                './gb.conf']

        self.cp = ConfigParser.SafeConfigParser()
        self.cp.read(conffiles)

        self.sensors = {}
        self.graphs = {}

        self.parse()
        self.validate()

    def parse(self):
        for section in self.cp.sections():
            # Stub out our graphs
            if section[0:5] == "graph":
                for name in [ "title", "sensors" ]:
                    if not self.cp.has_option(section, name):
                        raise ConfigError(
                                "Section {} missing \"{}\"".format(section,
                                    name))
                self.graphs[section] = {}
                self.graphs[section]["sensors"] = self.cp.get(section,
                        "sensors").split(",")
                self.graphs[section]["title"] = self.cp.get(section, "title")
            # Assume we're a sensor
            else:
                for name in [ "title", "type", "unit", "id" ]:
                    if not self.cp.has_option(section, name):
                        raise ConfigError(
                                "Section {} missing \"{}\"".format(section,
                                    name))
                self.sensors[section] = {}
                for (name, value) in self.cp.items(section):
                    self.sensors[section][name] = value

    def validate(self):
        for (name, value) in self.graphs.items():
            for sensor in value['sensors']:
                if not sensor in self.sensors.keys():
                    raise ConfigError(
                            "Error in {}: No such Sensor {}".format(name,
                                sensor))

if __name__ == "__main__":
    config = Config()
    print repr(config.sensors)
    print repr(config.graphs)

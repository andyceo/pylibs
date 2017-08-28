#!/usr/bin/python3

import configparser
import os
import sys

config = configparser.ConfigParser()
config_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
config.read([config_dir + '/config-sample.ini', config_dir + '/config.ini'])

for section in config.sections():
    for (k, v) in config.items(section):
        key = k[:-5]
        if k[-5:] == '_file' and not config.has_option(section, key):
            with open(config[section][k], 'r') as file:
                config[section][key] = file.read().strip(' \t\n\r')

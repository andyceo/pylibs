#!/usr/bin/python3

import configparser
import os
import sys

config = configparser.ConfigParser()
config_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
config.read([config_dir + '/config-sample.ini', config_dir + '/config.ini'])

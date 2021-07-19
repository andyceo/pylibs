#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Some common work for configuration through config file and environment variables."""
import configparser
import logging
import os
import sys
from deepmerge import always_merger
from singleton import Singleton


def _flatten_vars_dict(d, previous_key, flattened_dict):
    """Call this like that: variables = _flatten_dict(somevars, '', {})"""
    if isinstance(d, dict):
        for k in d:
            new_key = '{}_{}'.format(previous_key, k) if len(previous_key) > 0 else k
            _flatten_vars_dict(d[k], new_key, flattened_dict)
    else:
        pk = previous_key.upper()
        flattened_dict[pk] = os.environ.get(pk, d)

        # automatic type conversion
        t = type(d)
        if d is not None and flattened_dict[pk] != d and t in (str, int, float):
            flattened_dict[pk] = t(flattened_dict[pk])

        # load '_file' value into apropriate variable
        if pk[-5:] == '_FILE' and flattened_dict[pk]:
            substituted_k = pk[:-5]
            if substituted_k not in flattened_dict or substituted_k not in os.environ:
                filename = os.environ.get(pk, flattened_dict[pk])
                try:
                    with open(filename) as f:
                        flattened_dict[substituted_k] = f.read().strip(' \t\n\r')
                except EnvironmentError:
                    logging.getLogger().warning(
                        'File {} can not be open! It may cause further errors!'.format(filename))

    return flattened_dict


def _environ_lookup(section: str, key: str, value, d: dict):
    """
    Seek for appropriate environment variable and return it's value if found, value otherwise.
    Also change passed dictionary d to store variable and it's value.
    If environment variable not exists, but value is None, variable does not stored into dict and None returned.

    :param d: Dictionary where to store passed variable
    :param section: ConfigParser section name
    :param key: Key in ConfigParser section
    :param value: Value that was read from ConfigParser[section][key]
    :return: Value of SECTION_KEY environment variable if it exists, value otherwise
    """
    s = section.lower()
    k = key.lower()
    envvar = section.upper() + '_' + k.upper()
    if envvar in os.environ:
        d[s][k] = os.environ[envvar]
        return os.environ[envvar]
    elif value is not None:
        d[s][k] = value
        return value
    else:
        return None


def parse(defaults_as_section=False) -> dict:
    """This function parse config and return it as dictionary, taking in account environments variables.
    :rtype: dict
    """
    config = configparser.ConfigParser()
    config_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    config.read([config_dir + '/config-sample.ini', config_dir + '/config.ini'])
    config_defaults = config.defaults()

    config_dict = {}

    for section in config.sections():
        section_lower = section.lower()
        config_dict[section_lower] = {}

        for k, v in config.items(section):
            if defaults_as_section and k in config_defaults and v == config_defaults[k]:
                continue

            k_lower = k.lower()
            _environ_lookup(section, k, v, config_dict)

            if k_lower[-5:] == '_file':
                k_before_file = k[:-5]
                if config.has_option(section, k_before_file):
                    v_before_file = config.get(section, k_before_file)
                else:
                    v_before_file = None

                if _environ_lookup(section, k_before_file, v_before_file, config_dict) is None:
                    try:
                        with open(config[section][k], 'r') as file:
                            config_dict[section_lower][k_before_file.lower()] = file.read().strip(' \t\n\r')
                    except EnvironmentError:
                        logging.getLogger().warning(
                            'File {} can not be open! It may cause further errors!'.format(config[section][k]))

    if defaults_as_section:
        config_dict['DEFAULT'] = {}
        for k, v in config_defaults.items():
            environ_value = _environ_lookup('DEFAULT', k, None, config_dict)
            config_dict['DEFAULT'][k.lower()] = environ_value if environ_value is not None else v

    return config_dict


def group_envars(evs, prefix):
    """Group envars on given prefix and return dictionary with elements without prefix and lowercased keys"""
    res = {}
    p = prefix.upper() + '_'
    plen = len(p)
    for vk in evs:
        if vk[:plen] == p:
            nk = vk[plen:].lower()
            res[nk] = evs[vk]
    return res


def getenvars(variables=None):
    defaults = {
        'bitfinex': {
            'api':
                {
                    'key': '',
                    'key_file': None,
                    'secret': '',
                    'secret_file': None,
                }
        },

        'influxdb': {
            'host': 'influxdb',
            'port': 8086,
            'timeout': 5,
            'username': None,
            'password': None,
            'password_file': None,
            'database': None,
            'measurement': None,
        },

        'logging': {
            'level': logging.INFO,
            'format': "[%(asctime)s] %(levelname)s [%(name)s.%(module)s.%(funcName)s:%(lineno)d] %(message)s",
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },

        'mongodb': {
            'host': 'mongodb',
            'port': 27017,
            'username': None,
            'password': None,
            'password_file': None,
            'database': None,
        },

        'mysql': {
            'host': 'mysql',
            'port': 3306,
            'username': None,
            'password': None,
            'password_file': None,
            'database': None,
            "charset": "utf8mb4",
        },

        'delay': 30,

        'test': 'sometest'
    }
    always_merger.merge(defaults, variables if variables else {})  # merge given dict with defaults
    variables = _flatten_vars_dict(defaults, '', {})
    return variables


def get_basic_logger(evs):
    """Set logging module basic config and return default logger"""
    logging.basicConfig(
        level=evs['LOGGING_LEVEL'],
        format=evs['LOGGING_FORMAT'],
        datefmt=evs['LOGGING_DATEFMT']
    )
    return logging.getLogger()


class ConfigHelper(metaclass=Singleton):
    """This is helper singleton class that aimed to help include parsed config in other app parts and modules"""
    _evs = None
    _logger = None

    def __init__(self):
        # the following is the fix for the case when no logger exists when creating instance of this class
        # this happens when this class instance creates very first
        # @todo maybe rewrite to setter/getter pattern for evs, logger?
        # @see https://stackoverflow.com/questions/2627002/whats-the-pythonic-way-to-use-getters-and-setters
        # @see https://www.python-course.eu/python3_properties.php
        # @see https://www.geeksforgeeks.org/getter-and-setter-in-python/
        self.get_evs()
        self.get_logger()

        self._logger.info('Singleton instance of {} class initialized!'.format(self.__class__.__name__))

    def get_evs(self, default_envars_function=None):
        """Return current parsed environment variables"""
        if self._evs is None:
            if default_envars_function is None:
                self._evs = getenvars(parse(True))
            else:
                self._evs = getenvars(default_envars_function(parse(True)))
        return self._evs

    def get_logger(self, logger_name=''):
        """Return default logger if logger_name not passed"""
        if self._logger is None:
            self._logger = get_basic_logger(self._evs)
        return self._logger if not logger_name else logging.getLogger(logger_name)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Some common work for configuration through config file and environment variables."""

import configparser
import logging
import os
import sys
from deepmerge import always_merger


def _flatten_vars_dict(d, previous_key, flattened_dict):
    """Call this like that: variables = _flatten_dict(somevars, '', {})"""
    if isinstance(d, dict):
        for k in d:
            new_key = '{}_{}'.format(previous_key, k) if len(previous_key) > 0 else k
            _flatten_vars_dict(d[k], new_key, flattened_dict)
    else:
        pk = previous_key.upper()
        flattened_dict[pk] = os.environ.get(pk, d)

        t = type(d)
        if d is not None and flattened_dict[pk] != d and t in (str, int, float):
            flattened_dict[pk] = t(flattened_dict[pk])

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
            if defaults_as_section and k in config_defaults:
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
                    with open(config[section][k], 'r') as file:
                        config_dict[section_lower][k_before_file.lower()] = file.read().strip(' \t\n\r')

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

        'delay': 30,

        'test': 'sometest'
    }

    always_merger.merge(defaults, variables if variables else {})  # merge given dict with defaults
    variables = _flatten_vars_dict(defaults, '', {})
    for k in variables:
        if k[-5:] == '_FILE' and variables[k]:
            substituted_k = k[:-5]
            if substituted_k not in variables or not variables[substituted_k]:
                with open(variables[k]) as f:
                    variables[substituted_k] = f.read().strip(' \t\n\r')
    return variables


# @TODO this is done for compatibility reasons, remove when update all projects that use it and leave only functions
config = parse(True)


if __name__ == '__main__':
    a = {'users': None}
    print(getenvars(a))

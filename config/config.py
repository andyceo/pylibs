#!/usr/bin/python3

import configparser
import os
import sys


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


# @TODO this is done for compatibility reasons, remove when update all projects that use it and leave only functions
config = parse(True)

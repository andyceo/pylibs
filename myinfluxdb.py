from influxdb import InfluxDBClient
from pylibs import config


def connect(section):
    """Connect to the InfluxDB"""
    host = config[section]['host']
    port = int(config[section]['port'])
    username = config[section]['username']
    password = config[section]['password']
    db = config[section]['database'] if config.has_option(section, 'database') else config[section]['db']
    client = InfluxDBClient(host, port, username, password, db)
    return client

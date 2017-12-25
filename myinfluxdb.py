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


def write(client, points, time_precision=None):
    batch_size = 10000
    l = len(points)
    for i in range(0, l, batch_size):
        end = i + batch_size - 1
        end = l if end > l else end
        client.write_points(points[i:end], time_precision=time_precision)

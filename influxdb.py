import argparse
import copy
import os
from influxdb import InfluxDBClient


def connect(config):
    """Connect to the InfluxDB"""
    host = config['host'] if 'host' in config else 'localhost'
    port = int(config['port']) if 'port' in config else 8086
    username = config['username']
    password = config['password']
    database = config['database']
    return InfluxDBClient(host, port, username, password, database)


def batch_write_points(client, points, time_precision=None):
    batch_size = 10000
    l = len(points)
    for i in range(0, l, batch_size):
        end = i + batch_size - 1
        end = l if end > l else end
        client.write_points(points[i:end], time_precision=time_precision)


def move_points(source, dest):
    """
    This function helps transfer points from one database (and/or measurement) to another one. Here is the demo script
    using that function:


    import pylibs

    source = {
        'client': pylibs.connect({
            'host': 'influxdb_source',
            'username': 'user1',
            'password': 'super_secret_password',
            'database': 'some_database'
        }),
        'measurement': 'dockerhub',
        'fields': ['field_1', 'field_2', 'another_field'],
        'tags': ['tag_1', 'tag_2']
    }

    dest = pylibs.connect({
        'host': 'influxdb_dest',
        'username': 'user2',
        'password': 'another_super_secret_password',
        'database': 'another_database'
    })

    pylibs.move_points(source, dest)


    :param source: Dictionary with source measurement description.
    :param dest: Destination client or dictionary with destination measurement description.
    :return:
    """

    if not isinstance(dest, dict):
        dest = {'client': dest}

    if 'client' not in source or 'client' not in dest:
        print("Source and destinations clients must be passed in!")
        exit(1)

    if 'measurement' not in source:
        print("Source measurement must be passed in!")
        exit(2)
    elif 'measurement' not in dest:
        dest['measurement'] = source['measurement']

    res = source['client'].query("SELECT * FROM {}".format(source['measurement']))

    points = []
    point_template = {
        "time": None,
        "measurement": dest['measurement'],
        "tags": {},
        "fields": {},
    }
    for point in res.get_points():
        point_raw = copy.deepcopy(point_template)
        point_raw['time'] = point['time']
        for meta_key in ['fields', 'tags']:
            for key in source[meta_key]:
                point_raw[meta_key][key] = point[key]
        points.append(point_raw)

    batch_write_points(dest['client'], points)


def argparse_add_influxdb_options(parser: argparse.ArgumentParser):
    """Add InfluxDB connection parameters to given parser. Also read environment variables for defaults"""

    parser.add_argument('--influxdb-host', metavar='HOST', default=os.environ.get('INFLUXDB_HOST', 'localhost'),
                        help='InfluxDB host name')

    parser.add_argument('--influxdb-port', metavar='PORT', default=os.environ.get('INFLUXDB_PORT', 8086),
                        help='InfluxDB host port')

    parser.add_argument('--influxdb-user', metavar='USER', default=os.environ.get('INFLUXDB_USER', None),
                        help='InfluxDB user')

    parser.add_argument('--influxdb-password', metavar='PASSWORD', default=os.environ.get('INFLUXDB_PASSWORD', None),
                        help='InfluxDB user password')

    parser.add_argument('--influxdb-password-file', metavar='FILE', default=os.environ.get(
        'INFLUXDB_PASSWORD_FILE', None), help='Filename contains InfluxDB user password')

    parser.add_argument('--influxdb-database', metavar='DATABASE', default=os.environ.get('INFLUXDB_DATABASE', None),
                        help='InfluxDB database to connect to')

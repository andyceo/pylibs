import argparse
import copy
import os
import time
import utils
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError


def connect(config):
    """Connect to the InfluxDB"""
    host = config['host'] if 'host' in config else 'localhost'
    port = int(config['port']) if 'port' in config else 8086
    timeout = int(config['timeout']) if 'timeout' in config else 5
    username = config['username']
    password = config['password']
    database = config['database']
    return InfluxDBClient(host=host, port=port, username=username, password=password, database=database,
                          timeout=timeout)


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


def timestamp_to_influxdb_format(timestamp=time.time()) -> int:
    """
    Convert timestamp to integer of InfluxDB format.

    :param timestamp: Datetime in timestamp format (number of seconds that elapsed since
        00:00:00 Coordinated Universal Time (UTC), Thursday, 1 January 1970. Can be string, int or float
    :return: Integer that ready to use in influxdb.client.write_points() function without precision parameter
    """
    return round(float(timestamp) * 1000000000)


def write_points_with_exception_handling(client, points, time_precision=None):
    try:
        return client.write_points(points, time_precision=time_precision)
    except InfluxDBClientError as err:
        utils.message('!Nothing saved as InfluxDB client error happens: {}'.format(err))
    except InfluxDBServerError as err:
        utils.message('!Nothing saved as InfluxDB server error happens: {}'.format(err))


if __name__ == '__main__':
    test = [
        {'input': '1526041380.9045842', 'output': 1526041380904584200}
    ]
    for t in test:
        # @todo find why test did not pass, transformed = 1526041380904584192 if use round() or int()
        transformed = timestamp_to_influxdb_format(t['input'])
        is_ok = 'OK' if transformed == t['output'] else 'FAIL'
        is_eq = '==' if transformed == t['output'] else '!='
        print("{}: {}({}) -> {}({}) {} {}".format(is_ok, t['input'], type(t['input']), transformed, type(transformed), is_eq, t['output']))

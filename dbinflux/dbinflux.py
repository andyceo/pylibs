#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provide some extra functions to work with InfluxDB."""
import argparse
import copy
import csv
import os
import logging
import time
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError


def connect(config) -> InfluxDBClient:
    """Connect to the InfluxDB with given config"""
    host = config['host'] if 'host' in config else \
        config['INFLUXDB_HOST'] if 'INFLUXDB_HOST' in config else 'localhost'

    port = int(config['port']) if 'port' in config else \
        int(config['INFLUXDB_PORT']) if 'INFLUXDB_PORT' in config else 8086

    timeout = int(config['timeout']) if 'timeout' in config else \
        int(config['INFLUXDB_TIMEOUT']) if 'INFLUXDB_TIMEOUT' in config else 5

    username = config['username'] if 'username' in config else config['INFLUXDB_USERNAME']
    password = config['password'] if 'password' in config else config['INFLUXDB_PASSWORD']
    database = config['database'] if 'database' in config else config['INFLUXDB_DATABASE']
    return InfluxDBClient(host=host, port=port, username=username, password=password, database=database,
                          timeout=timeout)


def dump_measurement_csv(client, measurement, chunk_size=500, logger=None, show_cli_cmd=False):
    """Dump given measurement to csv file"""
    if not logger:
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger()

    query = "SELECT * FROM {}".format(measurement)

    if show_cli_cmd:
        logger.info("0. Stop inserting in measurement '%s'", measurement)
        logger.info("1. Execute following command in InfluxDB CLI to get same output faster:")
        logger.info("    influx -database '%s' -username '%s' -password '%s' -execute '%s LIMIT 2' -format csv > "
                    "/tmp/%s.csv", client._database, client._username, client._password, query, measurement)
        logger.info("2. Execute 1 once again and check files hashes, to be sure no new data was saved during export")
        logger.info("   Also, you may want count points number with 'wc -l /tmp/%s.csv'", measurement)
        logger.info("3. Then transform csv file '%s.csv' -> '%s.txt' (line protocol file) with csv2lp() function",
                    measurement, measurement)
        logger.info("   Also, do any data transformation you want, for example, type conversion, etc")
        logger.info("4. Drop measurement: DROP MEASUREMENT %s", measurement)
        logger.info("5. And last, import data back into InfluxDB:")
        logger.info("    influx -username '%s' -password '%s' -import -pps 10000 -path=%s.txt",
                    client._username, client._password, measurement)
        logger.info("6. Check new measurement schema with:")
        logger.info("    influx -database '%s' -username '%s' -password '%s' -execute 'SHOW FIELD KEYS FROM %s'",
                    client._database, client._username, client._password, measurement)
        logger.info("    influx -database '%s' -username '%s' -password '%s' -execute 'SHOW TAG KEYS FROM %s'",
                    client._database, client._username, client._password, measurement)
        logger.info("    influx -database '%s' -username '%s' -password '%s' "
                    "-execute 'SHOW TAG VALUES FROM %s WITH KEY IN (...)'",
                    client._database, client._username, client._password, measurement)
    else:
        logger.info("Dumping measurement '%s' started...", measurement)
        logger.info("Start query '%s' with chunk size %d...", query, chunk_size)
        t0 = time.time()
        res = client.query(query, chunked=True, chunk_size=chunk_size)
        t1 = time.time()
        tdiff = t1-t0
        logger.info('End query. Time: %ds (%.2fm)', tdiff, tdiff/60)
        # @todo finish function (actually dump data)


def csv2lp(csv_filepath, tags_keys=None, database=None, retention_policy=None):
    """Transform given csv file into file protocol file. Run example:
    csv2lp('/root/bitfinex_ticker.csv', ['symbol'], 'alfadirect', 'alfadirect')"""
    tags_keys = tags_keys if tags_keys else []
    path, filename = os.path.split(csv_filepath)
    filename_wo_extension = os.path.splitext(os.path.basename(filename))[0]
    lp_filepath = path + '/' + filename_wo_extension + '.txt'
    with open(csv_filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        with open(lp_filepath, 'w') as lp:

            if database and retention_policy:
                lp.write('# DML\n')
                lp.write('# CONTEXT-DATABASE: {}\n'.format(database))
                lp.write('# CONTEXT-RETENTION-POLICY: {}\n\n'.format(retention_policy))

            for row in reader:
                tag_set = []
                for tag_key in tags_keys:
                    tag_set.append('{}={}'.format(tag_key, row[tag_key]))
                tag_set = ','.join(tag_set)

                field_set = []
                excludes = ['name', 'time'] + tags_keys
                for field_key, field_value in row.items():
                    if field_key not in excludes:
                        field_set.append('{}={}'.format(field_key, field_value))
                field_set = ','.join(field_set)

                name = row['name']
                time = row['time']
                lp.write('{},{} {} {}\n'.format(name, tag_set, field_set, time))


def batch_write_points(client, points, time_precision=None):
    batch_size = 10000
    l = len(points)
    for i in range(0, l, batch_size):
        end = i + batch_size - 1
        end = l if end > l else end
        client.write_points(points[i:end], time_precision=time_precision)


def move_points(source, dest):
    """This function helps transfer points from one database (and/or measurement) to another one. Here is the demo
    script using that function:


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
    """Convert timestamp to integer of InfluxDB format.

    :param timestamp: Datetime in timestamp format (number of seconds that elapsed since
        00:00:00 Coordinated Universal Time (UTC), Thursday, 1 January 1970. Can be string, int or float
    :return: Integer that ready to use in influxdb.client.write_points() function without precision parameter
    """
    return round(float(timestamp) * 1000000000)


def write_points_with_exception_handling(client, points, time_precision=None, logger=None):
    if not logger:
        logger = logging.getLogger()
    try:
        return client.write_points(points, time_precision=time_precision)
    except InfluxDBClientError as e:
        logger.warning('Nothing saved as InfluxDB client error happens: %s', getattr(e, 'message', repr(e)))
    except InfluxDBServerError as e:
        logger.warning('Nothing saved as InfluxDB server error happens: %s', getattr(e, 'message', repr(e)))


def get_measurements(client, database: str) -> list:
    """Return the list of measurements in given database"""
    return [m['name'] for m in client.query('SHOW MEASUREMENTS ON {}'.format(database)).get_points()]


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

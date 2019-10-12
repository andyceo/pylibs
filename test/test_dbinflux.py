import copy
import dbinflux
import unittest
from influxdb import InfluxDBClient


class TestDbInflux(unittest.TestCase):
    def are_idbc_objects_equal(self, first, second, msg=None):
        self.assertEqual(type(first), type(second))
        self.assertEqual(first._host, second._host)
        self.assertEqual(first._port, second._port)
        self.assertEqual(first._timeout, second._timeout)
        self.assertEqual(first._username, second._username)
        self.assertEqual(first._password, second._password)
        self.assertEqual(first._database, second._database)

    def test_connect(self):
        self.addTypeEqualityFunc(InfluxDBClient, self.are_idbc_objects_equal)

        cfg = {
            'host': 'localhost',
            'port': 123,
            'timeout': 1,
            'username': 'someuser',
            'password': 'somepass',
            'database': 'somedb',
        }

        evs = {
            'INFLUXDB_HOST': 'localhost_evs',
            'INFLUXDB_PORT': 1230,
            'INFLUXDB_TIMEOUT': 10,
            'INFLUXDB_USERNAME': 'someuser_evs',
            'INFLUXDB_PASSWORD': 'somepass_evs',
            'INFLUXDB_DATABASE': 'somedb_evs',
        }

        expected_result = InfluxDBClient(host=cfg['host'], port=cfg['port'], username=cfg['username'],
                                         password=cfg['password'], database=cfg['database'], timeout=cfg['timeout'])
        result = dbinflux.connect(cfg)
        self.assertEqual(result, expected_result)

        cfg2 = copy.deepcopy(cfg)
        del cfg2['port'], cfg2['timeout']
        expected_result = InfluxDBClient(host='localhost', port=8086, username='someuser',
                                         password='somepass', database='somedb', timeout=5)
        result = dbinflux.connect(cfg2)
        self.assertEqual(result, expected_result)

        expected_result = InfluxDBClient(host=evs['INFLUXDB_HOST'], port=evs['INFLUXDB_PORT'],
                                         username=evs['INFLUXDB_USERNAME'], password=evs['INFLUXDB_PASSWORD'],
                                         database=evs['INFLUXDB_DATABASE'], timeout=evs['INFLUXDB_TIMEOUT'])
        result = dbinflux.connect(evs)
        self.assertEqual(result, expected_result)

        evs2 = copy.deepcopy(evs)
        del evs2['INFLUXDB_PORT'], evs2['INFLUXDB_TIMEOUT']
        expected_result = InfluxDBClient(host='localhost_evs', port=8086, username='someuser_evs',
                                         password='somepass_evs', database='somedb_evs', timeout=5)
        result = dbinflux.connect(evs2)
        self.assertEqual(result, expected_result)

        cfg_merged = {**cfg, **evs}
        expected_result = InfluxDBClient(host=cfg['host'], port=cfg['port'], username=cfg['username'],
                                         password=cfg['password'], database=cfg['database'], timeout=cfg['timeout'])
        result = dbinflux.connect(cfg_merged)
        self.assertEqual(result, expected_result)

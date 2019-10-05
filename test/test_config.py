import config
import copy
import unittest


class TestConfig(unittest.TestCase):
    def test_group_envars(self):
        evs = {
            'SOME_VAR': False,
            'INFLUXDB_HOST': 'localhost',
            'INFLUXDB_PORT': 123,
            'INFLUXDB__USERNAME': 'someuser',
        }

        expected_result = {
            'host': 'localhost',
            'port': 123,
            '_username': 'someuser',
        }

        res = config.group_envars(evs, 'influxdb')
        self.assertEqual(res, expected_result)

    def test_getenvars(self):
        expected_result = {
            'BITFINEX_API_KEY': '',
            'BITFINEX_API_SECRET': '',
            'INFLUXDB_HOST': 'influxdb',
            'INFLUXDB_PORT': 8086,
            'INFLUXDB_TIMEOUT': 5,
            'INFLUXDB_USERNAME': None,
            'INFLUXDB_PASSWORD': None,
            'INFLUXDB_PASSWORD_FILE': None,
            'INFLUXDB_DATABASE': None,
            'INFLUXDB_MEASUREMENT': None,
            'LOGGING_LEVEL': 20,
            'LOGGING_FORMAT': '[%(asctime)s] %(levelname)s [%(name)s.%(module)s.%(funcName)s:%(lineno)d] %(message)s',
            'LOGGING_DATEFMT': '%Y-%m-%d %H:%M:%S',
            'DELAY': 30,
            'TEST': 'sometest'
        }

        evs = config.getenvars()
        self.assertEqual(evs, expected_result)

        expected_result2 = copy.deepcopy(expected_result)
        expected_result2['BITFINEX_API_KEY'] = 'somekey'
        expected_result2['INFLUXDB_PORT'] = 123
        expected_result2['TEST'] = 'another test'
        evs = config.getenvars({
            'bitfinex': {
                'api': {
                    'key': 'somekey'
                }
            },
            'influxdb': {
                'port': 123
            },
            'test': 'another test'
        })
        self.assertEqual(evs, expected_result2)

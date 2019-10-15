import config
import copy
import os
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
            'BITFINEX_API_KEY_FILE': None,
            'BITFINEX_API_SECRET': '',
            'BITFINEX_API_SECRET_FILE': None,
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
            'MONGODB_HOST': 'mongodb',
            'MONGODB_PORT': 27017,
            'MONGODB_USERNAME': None,
            'MONGODB_PASSWORD': None,
            'MONGODB_PASSWORD_FILE': None,
            'MONGODB_DATABASE': None,
            'DELAY': 30,
            'TEST': 'sometest'
        }

        evs = config.getenvars()
        self.assertEqual(evs, expected_result)

        expected_result2 = copy.deepcopy(expected_result)
        expected_result2['BITFINEX_API_KEY'] = 'somekey'
        expected_result2['INFLUXDB_PORT'] = 123
        expected_result2['TEST'] = 'another test'
        expected_result2['DELAY'] = 12
        os.environ["DELAY"] = "12"
        defaults = {
            'bitfinex': {
                'api': {
                    'key': 'somekey'
                }
            },
            'influxdb': {
                'port': 123
            },
            'test': 'another test',
        }
        evs = config.getenvars(defaults)
        self.assertEqual(evs, expected_result2)

        expected_result3 = copy.deepcopy(expected_result2)
        filename = '/tmp/bfx_api_key_test'
        filecontent = 'BITFINEX_API_KEY_FILE_TEST_CONTENT'
        expected_result3['BITFINEX_API_KEY'] = filecontent
        expected_result3['BITFINEX_API_KEY_FILE'] = filename
        with open(filename, 'w') as f:
            f.write(filecontent)
            os.environ['BITFINEX_API_KEY_FILE'] = filename
        evs = config.getenvars(defaults)
        self.assertEqual(evs, expected_result3)

        expected_result4 = copy.deepcopy(expected_result3)
        another_content = 'ANOTHER_CONTENT!'
        expected_result4['BITFINEX_API_KEY'] = another_content
        os.environ['BITFINEX_API_KEY'] = another_content
        evs = config.getenvars(defaults)
        self.assertEqual(evs, expected_result4)
        os.remove(filename)

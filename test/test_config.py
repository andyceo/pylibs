import unittest
import config


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

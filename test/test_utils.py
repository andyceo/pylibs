import unittest
import utils


class TestUtils(unittest.TestCase):
    def test_timestamp2int(self):
        test_vector = {
            '123457869.0': 123457869,
            '123457869.1': 123457869,
            '123457869.8': 123457870,
            '123457869': 123457869,
            123457869: 123457869,
            123457869.0: 123457869,
            123457869.1: 123457869,
            123457869.8: 123457870
        }
        for k, expected_result in test_vector.items():
            result = utils.timestamp2int(k)
            self.assertEqual(result, expected_result)

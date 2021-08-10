import time
import unittest
import timefuncs


class TestTimefuncs(unittest.TestCase):
    def test_gmtdt(self):
        test_vector = [1596879145.5054562, 1596879145, 1436879145.12, 100000000]
        expected_results = ['2020-08-08T09:32:25+00:00', '2020-08-08T09:32:25+00:00', '2015-07-14T13:05:45+00:00',
                            '1973-03-03T09:46:40+00:00']
        for i in range(len(test_vector)):
            self.assertEqual(timefuncs.gmtdt(test_vector[i]), expected_results[i])

    def test_mstimestamp(self):
        ts = time.time()
        test_vector = {
            1628615834.9545038: 1628615834955, 1628615834.955: 1628615834955, 1628615834: 1628615834000,
            '1628615834.9545038': 1628615834955, '1628615834.955': 1628615834955, '1628615834': 1628615834000,
            ts: round(ts*1000)
        }
        for ts, expected_result in test_vector.items():
            self.assertEqual(timefuncs.mstimestamp(ts), expected_result)

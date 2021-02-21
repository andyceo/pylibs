import unittest
from historical import Timeframe, TimeframeError, TIMEFRAMES


class TestHistorical(unittest.TestCase):
    def test_timeframe(self):
        expected_results = [60, 300, 900, 1800, 3600, 10800, 21600, 43200, 86400, 604800, 1209600, 2592000]
        len_timeframes = len(TIMEFRAMES)
        len_results = len(expected_results)
        self.assertEqual(len_timeframes, len_results,
                         "Number of possible timeframes {} does not match with number of expected results {}".format(
                             len_timeframes, len_results))

        for i in range(len_timeframes):
            self.assertEqual(Timeframe.tfd(TIMEFRAMES[i]), expected_results[i],
                             "Duration of timeframe {} not match with expected result {}".format(TIMEFRAMES[i],
                                                                                                 expected_results[i]))

        tf_string = '1D'
        tf = Timeframe(tf_string)
        self.assertIsInstance(tf, Timeframe, "Timeframe does not create")
        self.assertEqual(tf.timeframe, tf_string, "Timeframe creation error")
        self.assertEqual(tf.duration, Timeframe.tfd(tf_string),
                         "Timeframe duration calc wrong during timeframe creation")

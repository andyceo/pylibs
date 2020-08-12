import unittest
from bitfinex import BitfinexHelper as bh


class TestBitfinex(unittest.TestCase):
    def test_tfd(self):
        tfs = bh.tfs()
        expected_results = [60, 300, 900, 1800, 3600, 10800, 21600, 43200, 86400, 604800, 1209600, 2592000]
        ltfs = len(tfs)
        ler = len(expected_results)
        self.assertEqual(ltfs, ler,
                         "Number of possible timeframes {} does not match with number of expected results {}".format(
                             ltfs, ler))

        for i in range(ltfs):
            self.assertEqual(bh.tfd(tfs[i]), expected_results[i],
                             "Duration of timeframe {} not match with expected result {}".format(tfs[i],
                                                                                                 expected_results[i]))

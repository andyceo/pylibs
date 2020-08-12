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

    def test_candle2dict(self):
        candles = [
            [1572566400000, 9186.6, 7599.8823169, 9645, 6618, 174626.20339216],
            [1588291200000, 8630.7, 9451.1, 10045, 8101, 274650.86988354]
        ]
        expected_results = [
            {'MTS': 1572566400000, 'OPEN': 9186.6, 'CLOSE': 7599.8823169, 'HIGH': 9645, 'LOW': 6618,
             'VOLUME': 174626.20339216},
            {'MTS': 1588291200000, 'OPEN': 8630.7, 'CLOSE': 9451.1, 'HIGH': 10045, 'LOW': 8101,
             'VOLUME': 274650.86988354}
        ]

        for i in range(len(candles)):
            self.assertEqual(bh.candle2dict(candles[i]), expected_results[i])

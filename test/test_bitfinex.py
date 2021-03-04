import unittest
from bitfinex import BitfinexHelper as bh
from bitfinex import BitfinexTimeframe
from timeframeds import TimeframeError


class TestBitfinex(unittest.TestCase):

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

    def test_bitfinex_timeframe(self):
        test_vector = {
            '1D': {'timeframe': '1D', 'duration': 24 * 60 * 60, 'is_allowed': True},
            '7D': {'timeframe': '7D', 'duration': 7 * 24 * 60 * 60, 'is_allowed': True},
            '1W': {'timeframe': '7D', 'duration': 7 * 24 * 60 * 60, 'is_allowed': False},
            '1m': {'timeframe': '1m', 'duration': 60, 'is_allowed': True},
        }

        # Test correct timeframes creation
        for tf_code, expected in test_vector.items():
            tf = BitfinexTimeframe(tf_code)
            self.assertIsInstance(tf, BitfinexTimeframe)
            self.assertEqual(tf.timeframe, expected['timeframe'])
            self.assertEqual(tf.duration, expected['duration'])
            self.assertEqual(BitfinexTimeframe.is_allowed(tf_code), expected['is_allowed'])

        # Test incorrect timeframe creation raises exception
        self.assertRaises(TimeframeError, BitfinexTimeframe, '1j')
        self.assertRaises(TimeframeError, BitfinexTimeframe, '4h')

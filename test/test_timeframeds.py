import secrets
import random
import unittest
from timeframeds import Timeframe, TimeframeError
from timeframeds import TimeframeDataset


class TestTimeframeds(unittest.TestCase):
    def test_timeframe(self):
        expected_results = {'1m': 60, '5m': 300, '15m': 900, '30m': 1800, '1h': 3600, '3h': 10800, '6h': 21600,
                            '12h': 43200, '1D': 86400, '7D': 604800, '1W': 604800, '14D': 1209600, '1M': 2592000}
        timeframes = Timeframe.timeframes()
        len_timeframes = len(timeframes)
        len_results = len(expected_results)
        self.assertEqual(len_timeframes, len_results,
                         "Number of possible timeframes {} does not match with number of expected results {}".format(
                             len_timeframes, len_results))

        for tf, d in expected_results.items():
            self.assertEqual(Timeframe.tfd(tf), d,
                             "Duration of timeframe {} not match with expected result {}".format(tf, d))

        # Test Timeframe.is_allowed()
        self.assertTrue(Timeframe.is_allowed('1m'))
        self.assertTrue(Timeframe.is_allowed('1W'))
        self.assertFalse(Timeframe.is_allowed('1j'))

        # Test Timeframe creation
        tf_string = '1D'
        tf = Timeframe(tf_string)
        self.assertIsInstance(tf, Timeframe, "Timeframe was not created properly")
        self.assertEqual(tf.timeframe, tf_string, "Timeframe.timeframe was not set properly")
        self.assertEqual(tf.duration, Timeframe.tfd(tf_string),
                         "Timeframe.duration calculate error during timeframe creation")

        # Test wrong timeframe raise exception
        self.assertRaises(TimeframeError, Timeframe, '1j')

    def test_timeframe_dataset(self):
        # Define test vector
        test_vector = [
            {
                'data': [
                    [1401580800000, 627.01, 640.79, 685, 522.15, 354190.51030868],
                    [1404172800000, 642.26, 580, 665, 561.47, 158002.70311825],
                    [1406851200000, 579.49, 477.81, 605.72, 443, 362044.27874483],
                    [1409529600000, 477.84, 387, 497.24, 365, 392789.90864222],
                    [1412121600000, 386.93, 336.82, 414.42, 275, 857821.63053737],
                ],
                'columns': ['Timestamp', 'Open', 'Close', 'High', 'Low', 'Volume'],
                'tsname': 'Timestamp',
                'timeframe': '1M',
                'tsunit': 'ms',
                'tscoef': 0.001,
                'tsindex': 0,
            },
            {
                'data': [
                    [11.95, 12.918, 1457740800, 13.45, 11.95, 237.77704100000005],
                    [13.45, 14.456, 1457827200, 15.074, 13.45, 379.2674689999997],
                    [14.531, 12.403, 1457913600, 14.95, 11.4, 27906.023460199984],
                    [12.42, 13.1, 1458000000, 13.421, 11.98, 13193.037191059999],
                    [13.1, 12.548, 1458086400, 13.89, 12.409, 6127.952784010013],
                    [12.548, 11.06, 1458172800, 12.62, 10.436, 26283.32875591992],
                    [11.08, 10.99, 1458259200, 11.198, 8.338, 45397.8284726099],
                    [10.99, 10.573, 1458345600, 11.17, 9.776, 20588.722359510015],
                    [10.589, 10.268, 1458432000, 10.881, 9.559, 9578.361702900014],
                    [10.219, 11.8, 1458518400, 12.048, 10.14, 11712.711932110005],
                ],
                'columns': ['Open', 'Close', 'Timestamped', 'High', 'Low', 'Volume'],
                'tsname': 'Timestamped',
                'timeframe': '1D',
                'tsunit': 's',
                'tscoef': 1,
                'tsindex': 2
            }
        ]

        # Test creation of empty TimeframeDataset
        for t in test_vector:
            ds = TimeframeDataset(data=[], columns=t['columns'], tsname=t['tsname'], timeframe=t['timeframe'],
                                  tsunit=t['tsunit'])
            self.assertIsInstance(ds, TimeframeDataset, "Empty TimeframeDataset was not created properly")
            self.assertEqual(ds.data, [])
            self.assertEqual(len(ds), 0)

        # Test TimeframeDataset creation and TimeframeDataset methods and attributes
        for t in test_vector:
            ds = TimeframeDataset(data=t['data'], columns=t['columns'], tsname=t['tsname'], timeframe=t['timeframe'],
                                  tsunit=t['tsunit'])
            self.assertIsInstance(ds, TimeframeDataset, "TimeframeDataset was not created properly")
            self.assertEqual(ds, t['data'])
            self.assertEqual(ds.data, t['data'])
            self.assertEqual(len(ds), len(t['data']))
            self.assertEqual(len(ds.data), len(t['data']))
            self.assertEqual(ds.columns, t['columns'])
            self.assertEqual(ds.tsname, t['tsname'])
            self.assertEqual(ds.tsindex, t['tsindex'])
            self.assertIsInstance(ds.timeframe, Timeframe)
            self.assertEqual(ds.timeframe.timeframe, t['timeframe'])
            self.assertEqual(ds.tsunit, t['tsunit'])
            self.assertAlmostEqual(ds.tscoef, t['tscoef'])

            # Test TimeframeDataset.data attribute and object indexing the same as object.data indexing and slicing
            random_index1 = secrets.randbelow(len(t['data']))
            self.assertEqual(ds[random_index1], t['data'][random_index1])
            self.assertEqual(ds.data[random_index1], t['data'][random_index1])

            random_index2 = random.randrange(len(ds))
            self.assertEqual(ds[random_index2], t['data'][random_index2])
            self.assertEqual(ds.data[random_index2], t['data'][random_index2])

            from_index = min(random_index1, random_index2)
            to_index = max(random_index1, random_index2)

            slice = ds[from_index:to_index]
            self.assertIsInstance(slice, TimeframeDataset)
            self.assertEqual(slice, t['data'][from_index:to_index])

            slice_data = ds.data[from_index:to_index]
            self.assertIsInstance(slice_data, list)
            self.assertEqual(slice_data, t['data'][from_index:to_index])

            # Test TimeframeDataset.is_ok_static() and .is_ok() methods
            self.assertTrue(TimeframeDataset.is_data_ok(t['data'], t['columns'], t['tsname']))
            self.assertTrue(ds.is_ok())

            # Test TimeframeDataset.get_dict(), dict2list and .get_timestamp() methods
            for index in [2, 4, -1]:
                expected = int(t['data'][index][t['columns'].index(t['tsname'])] * t['tscoef'])
                result = ds.get_timestamp(index)
                self.assertEqual(result, expected)

                expected = {column: t['data'][index][idx] for idx, column in enumerate(t['columns'])}
                result = ds.get_dict(index)
                self.assertEqual(result, expected)

                result = ds.dict2list(expected)
                self.assertEqual(result, t['data'][index])

            self.assertEqual(ds.get_dict(), expected)

            # Test TimeframeDataset.is_inside() method
            index = 1
            timestamp = int(t['data'][index][t['columns'].index(t['tsname'])] * t['tscoef'])
            self.assertTrue(ds.is_inside(timestamp, index))
            self.assertTrue(ds.is_inside(timestamp+1, index))
            self.assertTrue(ds.is_inside(timestamp+10, index))

            timestamp = int(t['data'][index+1][t['columns'].index(t['tsname'])] * t['tscoef'])
            self.assertFalse(ds.is_inside(timestamp, index))
            self.assertTrue(ds.is_inside(timestamp, index+1))

            # Test TimeframeDataset.is_last_closed() method
            self.assertTrue(ds.is_last_closed())

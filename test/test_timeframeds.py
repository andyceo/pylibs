import collections
import secrets
import random
import unittest
from timeframeds import Timeframe, TimeframeError
from timeframeds import TimeframeDataset


class TestTimeframeds(unittest.TestCase):
    def test_timeframe(self):
        test_vector = collections.OrderedDict()
        test_vector['1m'] = {
            'duration': 60, 'period': 1, 'timecode': 'm',
            'borders': [
                {'timestamp': 1614973900,
                 'result': {'start': 1614973860, 'end': 1614973920, 'iso_start': '2021-03-05T19:51'}},
                {'timestamp': 1614973401.1, 'result': {'start': 1614973380, 'end': 1614973440}},
                {'timestamp': 1614973740, 'result': {'start': 1614973740, 'end': 1614973800}},
            ],
            'fmt': [
                {'timestamp': 1614973900, 'result': '2021.03.05 19:51'},
                {'timestamp': 1614973401.1, 'result': '2021.03.05 19:43'},
                {'timestamp': 1614973401.1, 'fmt': 'iso', 'result': '2021-03-05T19:43:21+00:00'},
            ]}
        test_vector['5m'] = {'duration': 300, 'period': 5, 'timecode': 'm', 'borders': [
            {'timestamp': 1613974900, 'result': {'start': 1613974800, 'end': 1613975100}}]}
        test_vector['15m'] = {'duration': 900, 'period': 15, 'timecode': 'm', 'borders': [
            {'timestamp': 1614973344, 'result': {'start': 1614972600, 'end': 1614973500}}]}
        test_vector['30m'] = {'duration': 1800, 'period': 30, 'timecode': 'm', 'borders': [
            {'timestamp': 1613976000, 'result': {'start': 1613975400, 'end': 1613977200}}]}
        test_vector['1h'] = {
            'duration': 3600, 'period': 1, 'timecode': 'h',
            'borders': [{'timestamp': 1613990000, 'result': {'start': 1613988000, 'end': 1613991600}}],
            'fmt': [{'timestamp': 1613990000, 'result': '2021.02.22 10:33'}],
        }
        test_vector['3h'] = {'duration': 10800, 'period': 3, 'timecode': 'h', 'borders': [
            {'timestamp': 1613984581, 'result': {'start': 1613984400, 'end': 1613995200}}]}
        test_vector['4h'] = {'duration': 14400, 'period': 4, 'timecode': 'h'}
        test_vector['6h'] = {'duration': 21600, 'period': 6, 'timecode': 'h'}
        test_vector['12h'] = {'duration': 43200, 'period': 12, 'timecode': 'h'}
        test_vector['1D'] = {'duration': 86400, 'period': 1, 'timecode': 'D',
                             'fmt': [{'timestamp': 1613990000, 'result': '2021.02.22'}],}
        test_vector['7D'] = {'duration': 604800, 'period': 7, 'timecode': 'D'}
        test_vector['1W'] = {'duration': 604800, 'period': 1, 'timecode': 'W'}
        test_vector['14D'] = {'duration': 1209600, 'period': 14, 'timecode': 'D'}
        test_vector['1M'] = {'duration': 2592000, 'period': 1, 'timecode': 'M'}

        timecodes = {}  # construct expected result timecodes in loop
        for tfs, props in test_vector.items():
            if props['timecode'] not in timecodes and tfs[0] == '1' and tfs[1] not in '0123456789':
                timecodes[props['timecode']] = props['duration']

            # Test Timeframe creation
            tf = Timeframe(tfs)
            self.assertIsInstance(tf, Timeframe)
            self.assertEqual(tf.timeframe, tfs)
            self.assertEqual(tf.duration, props['duration'])
            self.assertEqual(tf.timecode, props['timecode'])
            self.assertEqual(tf.period, props['period'])
            self.assertTrue(Timeframe.is_allowed(tfs))

            # Test .borders() method for the test vectors containing data for such test
            if 'borders' in props:
                for item in props['borders']:
                    res = tf.borders(item['timestamp'])
                    self.assertIsInstance(res, dict)
                    self.assertEqual(len(res), 10)
                    self.assertIn('start', res)
                    self.assertIn('end', res)
                    self.assertIn('iso_start', res)
                    self.assertIn('iso_end', res)
                    self.assertIn('iso_timestamp', res)
                    self.assertIn('secs_passed', res)
                    self.assertIn('secs_remain', res)
                    self.assertIn('pcnt_passed', res)
                    self.assertIn('pcnt_remain', res)
                    self.assertIn('timestamp', res)
                    for k, v in item['result'].items():
                        self.assertEqual(res[k], v)

            # Test .fmt() method for the test vectors containing data for such test
            if 'fmt' in props:
                for item in props['fmt']:
                    res = tf.fmt(item['timestamp'], fmt=item['fmt'] if 'fmt' in item else None)
                    self.assertIn(res, item['result'])

        # Test allowed timeframes
        self.assertEqual(Timeframe.timeframes(), tuple(test_vector.keys()))

        # Test allowed timeframe timecodes
        self.assertEqual(Timeframe.timecodes(), timecodes)

        # Test Timeframe.is_allowed() for wrong timestamp
        self.assertFalse(Timeframe.is_allowed('1j'))

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
            random_column_index = random.randrange(len(t['columns']))

            random_index1 = secrets.randbelow(len(t['data']))
            self.assertEqual(ds[random_index1], t['data'][random_index1])
            self.assertEqual(ds.data[random_index1], t['data'][random_index1])
            self.assertEqual(ds[random_index1][random_column_index], t['data'][random_index1][random_column_index])
            self.assertEqual(ds.data[random_index1][random_column_index], t['data'][random_index1][random_column_index])

            random_index2 = random.randrange(len(ds))
            self.assertEqual(ds[random_index2], t['data'][random_index2])
            self.assertEqual(ds.data[random_index2], t['data'][random_index2])
            self.assertEqual(ds[random_index2][random_column_index], t['data'][random_index2][random_column_index])
            self.assertEqual(ds.data[random_index2][random_column_index], t['data'][random_index2][random_column_index])

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

            # Tests TimeframeDataset.is_continuous() method
            if ds.timeframe.timecode != 'M':  # skip that test for months timeframes
                self.assertTrue(ds.is_continuous())
                ds[-1][ds.tsindex] += 1
                self.assertFalse(ds.is_continuous())

import json
import secrets
import random
import unittest
from timeframeds import Timeframe, TimeframeError
from timeframeds import TimeframeDataset


class TestTimeframeds(unittest.TestCase):
    def test_timeframe(self):
        testorder = ['1m', '5m', '15m', '30m', '1h', '3h', '4h', '6h', '12h', '1D', '7D', '1W', '14D', '1M']
        with open('test/test_vectors/timeframes.json') as json_file:
            test_vector = json.load(json_file)
            timecodes = {}  # construct expected result timecodes in loop

            for tfs in testorder:
                props = test_vector[tfs]
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
        with open('test/test_vectors/timeframedatasets.json') as json_file:
            test_vector = json.load(json_file)

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

            # Test (roughly) TimeframeDataset.get_dict() with given timestamp_format
            result = ds.get_dict(index, timestamp_format='timestamp')
            self.assertIsInstance(result[ds.tsname], int)
            result = ds.get_dict(index, timestamp_format='iso')
            self.assertIsInstance(result[ds.tsname], str)
            result = ds.get_dict(index, timestamp_format='human')
            self.assertIsInstance(result[ds.tsname], str)

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

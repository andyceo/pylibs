import unittest
from historical import Timeframe, TimeframeError, TIMEFRAMES
from historical import TimeframeDataset


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
        self.assertIsInstance(tf, Timeframe, "Timeframe was not created properly")
        self.assertEqual(tf.timeframe, tf_string, "Timeframe.timeframe was not set properly")
        self.assertEqual(tf.duration, Timeframe.tfd(tf_string),
                         "Timeframe.duration calculate error during timeframe creation")

    def test_timeframe_dataset(self):
        # Test TimeframeDataset creation
        data = [
            [1401580800000, 627.01, 640.79, 685, 522.15, 354190.51030868],
            [1404172800000, 642.26, 580, 665, 561.47, 158002.70311825],
            [1406851200000, 579.49, 477.81, 605.72, 443, 362044.27874483],
            [1409529600000, 477.84, 387, 497.24, 365, 392789.90864222],
            [1412121600000, 386.93, 336.82, 414.42, 275, 857821.63053737],
        ]
        columns = ['Timestamp', 'Open', 'Close', 'High', 'Low', 'Volume']
        tsname = 'Timestamp'
        timeframe = '1M'
        tsunit = 'ms'
        tscoef = 0.001
        tsindex = columns.index(tsname)
        ds = TimeframeDataset(data=data, columns=columns, tsname=tsname, timeframe=timeframe, tsunit=tsunit)
        self.assertIsInstance(ds, TimeframeDataset, "TimeframeDataset was not created properly")
        self.assertEqual(ds.data, data)
        self.assertEqual(ds.columns, columns)
        self.assertEqual(ds.tsname, tsname)
        self.assertEqual(ds.tsindex, tsindex)
        self.assertIsInstance(ds.timeframe, Timeframe)
        self.assertEqual(ds.timeframe.timeframe, timeframe)
        self.assertEqual(ds.tsunit, tsunit)
        self.assertAlmostEqual(ds.tscoef, tscoef)

        # Test TimeframeDataset.data attribute
        self.assertEqual(ds.data[3], data[3])

        # Test TimeframeDataset.is_ok_static() and .is_ok() methods
        self.assertTrue(TimeframeDataset.is_data_ok(data, columns, tsname))
        self.assertTrue(ds.is_ok())

        # Test TimeframeDataset.get_dict() and .get_timestamp() methods
        for index in [2, 4, -1]:
            expected = int(data[index][columns.index(tsname)] * tscoef)
            result = ds.get_timestamp(index)
            self.assertEqual(result, expected)

            expected = {column: data[index][idx] for idx, column in enumerate(columns)}
            result = ds.get_dict(index)
            self.assertEqual(result, expected)

        self.assertEqual(ds.get_dict(), expected)

        # Test TimeframeDataset.is_inside() method
        index = 1
        timestamp = int(data[index][columns.index(tsname)] * tscoef)
        self.assertTrue(ds.is_inside(timestamp, index))
        self.assertTrue(ds.is_inside(timestamp+1, index))
        self.assertTrue(ds.is_inside(timestamp+10, index))

        timestamp = int(data[index+1][columns.index(tsname)] * tscoef)
        self.assertFalse(ds.is_inside(timestamp, index))
        self.assertTrue(ds.is_inside(timestamp, index+1))

        # Test TimeframeDataset.is_last_closed() method
        self.assertTrue(ds.is_last_closed())

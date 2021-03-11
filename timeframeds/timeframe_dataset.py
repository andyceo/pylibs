#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module contain class HistoryDataset representing history data"""
import time
from collections import UserList
from timeframeds import Timeframe
from timefuncs import gmtdt


class TimeframeDatasetError(Exception):
    pass


class WrongTimestampUnit(Exception):
    pass


class TimeframeDataset(UserList):
    """Class for work with history data. Provide handy functions to work with history dataset"""

    @property
    def columns(self):
        return self.__columns

    @columns.setter
    def columns(self, columns):
        self.__columns = columns

    @property
    def tsname(self):
        return self.__tsname

    @tsname.setter
    def tsname(self, tsname):
        self.__tsname = tsname
        self.__tsindex = self.columns.index(tsname)

    @property
    def tsindex(self):
        return self.__tsindex

    @property
    def tscoef(self):
        return self.__tscoef

    @property
    def tsunit(self):
        return self.__tsunit

    @tsunit.setter
    def tsunit(self, tsunit):
        self.__tsunit = tsunit
        self.__tscoef = TimeframeDataset.timestamp_coefficient(tsunit)

    @property
    def timeframe(self):
        return self.__timeframe

    @timeframe.setter
    def timeframe(self, timeframe):
        self.__timeframe = timeframe

    def __init__(self, data: list, columns: list, tsname: str, timeframe: str, tsunit='s'):
        """data: list of lists or tuples; column_names: list of strings with column names"""
        if not TimeframeDataset.is_data_ok(data, columns, tsname):
            raise TimeframeDatasetError("Given data is not ok!")
        self.columns = columns
        self.tsname = tsname
        self.timeframe = Timeframe(timeframe)
        self.tsunit = tsunit
        super().__init__(data)

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__class__(self.data[i], columns=self.columns, tsname=self.tsname,
                                  timeframe=self.timeframe.timeframe, tsunit=self.tsunit)
        else:
            return self.data[i]

    def get_dict(self, index=-1, timestamp_format=None) -> dict:
        """Return dictionary with data from given index. Timestamp formatted according given timestamp_format"""
        d = {column: self.data[index][idx] for idx, column in enumerate(self.columns)}
        if timestamp_format == 'timestamp':
            int(d[self.tsname] * self.tscoef)
        elif timestamp_format == 'human':
            d[self.tsname] = self.timeframe.fmt(d[self.tsname] * self.tscoef)
        elif timestamp_format == 'iso':
            d[self.tsname] = self.timeframe.fmt(d[self.tsname] * self.tscoef, fmt='iso')
        return d

    def dict2list(self, d):
        """Return correct list that can be attached to self.data. This function is reverse to self.get_dict()"""
        lst = []
        for column in self.columns:
            if column in d:
                lst.append(d[column])
            else:
                raise TimeframeDatasetError("Given dictionary has no {} key!".format(column))
        return lst

    def get_timestamp(self, index=-1) -> int:
        """Return start timestamp from given index"""
        return int(self.data[index][self.tsindex] * self.tscoef)

    @staticmethod
    def is_data_ok(data: list, columns: list, tsname: str) -> bool:
        """Check given data is ok to be TimeframeDataset"""
        columns_len = len(columns)
        tsindex = columns.index(tsname)
        tsvalue = 0
        res = True
        for i, item in enumerate(data):
            res = res and (isinstance(item, list) or isinstance(item, tuple))  # check all data items are lists (tuples)
            res = res and (columns_len == len(item))  # check length for columns and each item
            res = res and (tsvalue < item[tsindex])  # check data is sorted by timestamp
            if not res:
                break
        return res

    @staticmethod
    def timestamp_coefficient(tsunit: str) -> float:
        """Calculate and return timestamp coefficient - timestamp must be multiplied at this coef and become measured in
        seconds"""
        coefs = {'s': 1, 'ms': 0.001}
        if tsunit not in coefs:
            raise WrongTimestampUnit("Timestamp unit is wrong or unknown!")
        return coefs[tsunit]

    def is_ok(self):
        """Same as TimeframeDataset.is_data_ok() but not static"""
        return TimeframeDataset.is_data_ok(self.data, self.columns, self.tsname)

    def is_inside(self, timestamp=time.time(), index=-1):
        """Chek given timestamp is inside given index"""
        return self.data[index][self.tsindex] * self.tscoef <= timestamp < \
               self.data[index][self.tsindex] * self.tscoef + self.timeframe.duration

    def is_last_closed(self):
        """Check last bar is closed (current timestamp is equal or bigger then closing timestamp)"""
        timestamp = time.time()
        last_timestamp = self.get_timestamp()
        tfduration = self.timeframe.duration
        return timestamp >= last_timestamp + tfduration

    def is_continuous(self):
        """Check dataset is continuous (has now holes in data, has points for all timestamps)"""
        ts = self.data[0][self.tsindex]
        for item in self.data[1:]:
            tsn = ts + self.timeframe.duration
            if item[self.tsindex] == tsn:
                ts = tsn
            else:
                return False
        return True

    def summary(self):
        """Return string with readable summary of TimeframeDataset. Usage: print(ds.summary())"""
        res = []
        cts = time.time()
        res.append('Summary for TimeframeDataset:')
        res.append('Current timestamp: {} (UTC {})'.format(cts, gmtdt(cts)))
        res.append('Dataset length: {}'.format(len(self.data)))
        res.append('Dataset is ok: {}'.format(self.is_ok()))
        res.append('Dataset columns: {}'.format(self.columns))
        res.append('Dataset timestamp column: {}'.format(self.tsname))
        res.append('Dataset timestamp column index: {}'.format(self.tsindex))
        res.append('First timestamp: {} (UTC {})'.format(self.get_timestamp(0), gmtdt(self.get_timestamp(0))))
        res.append('First item: {}'.format(self.data[0]))
        res.append('Last timestamp: {} (UTC {})'.format(self.get_timestamp(-1), gmtdt(self.get_timestamp(-1))))
        res.append('Last item: {}'.format(self.data[-1]))
        res.append('Timeframe: {}'.format(self.timeframe.timeframe))
        res.append('Timeframe duration, in seconds: {}'.format(self.timeframe.duration))
        res.append('Timestamp units: {}'.format(self.tsunit))
        res.append('Timestamp coefficient: {}'.format(self.tscoef))
        res.append('Last item is closed: {}'.format(self.is_last_closed()))
        return '\n'.join(res)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module contain class Timeframe representing typical exchanges timeframes"""
import time
import datetime
from timefuncs import gmtdt


class TimeframeError(Exception):
    pass


class Timeframe:

    @property
    def timeframe(self):
        return self.__timeframe

    @timeframe.setter
    def timeframe(self, timeframe):
        if not self.is_allowed(timeframe):
            raise TimeframeError('Unknown timeframe {}! Exiting...'.format(timeframe))
        self.__timeframe = timeframe
        tcp = self.parse(timeframe)
        self.__timecode = tcp['timecode']
        self.__period = tcp['period']
        self.__duration = tcp['duration']

    @property
    def timecode(self):
        return self.__timecode

    @property
    def period(self):
        return self.__period

    @property
    def duration(self):
        return self.__duration

    @staticmethod
    def timecodes() -> dict:
        """Return the string containing allowed timeframe time codes with duration, (m for minutes, D for days, etc)
        Unstable for months. @todo: fix months duration"""
        return {'m': 60, 'h': 60 * 60, 'D': 60 * 60 * 24, 'W': 7 * 60 * 60 * 24, 'M': 30 * 60 * 60 * 24}

    @staticmethod
    def timeframes():
        """Return the tuple containing allowed timeframe codes, started from very small (sorted ascending)"""
        return '1m', '5m', '15m', '30m', '1h', '3h', '4h', '6h', '12h', '1D', '7D', '1W', '14D', '1M'

    @staticmethod
    def is_allowed(timeframe: str):
        """Check if given timeframe is allowed"""
        return timeframe in Timeframe.timeframes()

    @staticmethod
    def parse(timeframe: str) -> dict:
        """Parse given timeframe string and return dictionary containing timecode, period and duration"""
        timecodes = Timeframe.timecodes()
        timecode = ''
        period = 0
        duration = 0
        for tc, d in timecodes.items():
            if tc in timeframe:
                timecode = tc
                period = int(timeframe.replace(tc, ''))
                duration = period * timecodes[tc]
                break
        if not timecode or not period or not duration:
            raise TimeframeError('Unknown timeframe {}! Exiting...'.format(timeframe))
        else:
            return {'timecode': timecode, 'period': period, 'duration': duration}

    def __init__(self, timeframe: str):
        self.timeframe = timeframe

    def borders(self, timestamp=time.time()) -> dict:
        """Return timeframe start, end timestamps (time borders) for the given timestamp (start <= timestamp < end)"""
        dtob = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc).replace(microsecond=0)
        if self.timecode == 'm':
            start_time_part = self.period * (dtob.minute // self.period)
            start_dtob = dtob.replace(minute=start_time_part, second=0, microsecond=0)
        elif self.timecode == 'h':
            start_time_part = self.period * (dtob.hour // self.period)
            start_dtob = dtob.replace(hour=start_time_part, minute=0, second=0, microsecond=0)
        elif self.timecode == 'D' and self.period == 1:
            start_dtob = dtob.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            raise TimeframeError('Can not get start date object for this timeframe!')
        start = int(start_dtob.timestamp())
        end = start + self.duration
        iso_ts = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc).isoformat()
        iso_start = datetime.datetime.fromtimestamp(start, tz=datetime.timezone.utc).isoformat()[:-9]
        iso_end = datetime.datetime.fromtimestamp(end, tz=datetime.timezone.utc).isoformat()[:-9]
        secs_passed = timestamp - start
        secs_remain = end - timestamp
        pcnt_passed = 100 * secs_passed / self.duration
        pcnt_remain = 100 * secs_remain / self.duration
        return {'start': start, 'end': end, 'iso_start': iso_start, 'iso_end': iso_end, 'iso_timestamp': iso_ts,
                'secs_passed': secs_passed, 'secs_remain': secs_remain, 'timestamp': timestamp,
                'pcnt_passed': pcnt_passed, 'pcnt_remain': pcnt_remain}

    def fmt(self, timestamp=time.time(), fmt='human') -> str:
        """Format given timestamp into the human-readable form based on current Timeframe"""
        s = gmtdt(timestamp)
        if fmt != 'iso':
            s = s.replace('-', '.').replace('T', ' ')
            if self.timecode in ['m', 'h']:
                s = s[:-9]
            else:
                s = s[:-15]
        return s

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module contain class Timeframe representing typical exchanges timeframes"""


class TimeframeError(Exception):
    pass


class Timeframe:

    @property
    def timeframe(self):
        return self.__timeframe

    @timeframe.setter
    def timeframe(self, timeframe):
        if not Timeframe.is_allowed(timeframe):
            raise TimeframeError('Unknown timeframe {}! Exiting...'.format(timeframe))
        self.__timeframe = timeframe
        self.__duration = Timeframe.tfd(self.__timeframe)

    @property
    def duration(self):
        return self.__duration

    @staticmethod
    def tfd(tf: str) -> int:
        """Calculate and return the timeframe duration in seconds. Unstable for monthes"""
        if 'm' in tf:
            tfd = int(tf.replace('m', '')) * 60
        elif 'h' in tf:
            tfd = int(tf.replace('h', '')) * 60 * 60
        elif 'D' in tf:
            tfd = int(tf.replace('D', '')) * 60 * 60 * 24
        elif 'W' in tf:
            tfd = int(tf.replace('W', '')) * 7 * 60 * 60 * 24
        elif 'M' in tf:
            tfd = int(tf.replace('M', '')) * 60 * 60 * 24 * 30
        else:
            raise TimeframeError('Unknown timeframe {}! Exiting...'.format(tf))
        return tfd

    @staticmethod
    def timeframes():
        """Return the tuple containing allowed timeframe codes"""
        return '1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1D', '7D', '1W', '14D', '1M'

    @staticmethod
    def is_allowed(timeframe: str):
        """Check if given timeframe is allowed"""
        return timeframe in Timeframe.timeframes()

    def __init__(self, timeframe: str):
        self.timeframe = timeframe

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Bitfinex helper class (contain useful static methods)"""


class BitfinexHelper:
    @staticmethod
    def tfs():
        """Return list of possible timeframes"""
        return ['1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1D', '7D', '14D', '1M']

    @staticmethod
    def tfd(tf: str) -> int:
        """Calculate and return the timeframe duration in seconds. Unstable for monthes"""
        if 'm' in tf:
            tfd = int(tf.replace('m', '')) * 60
        elif 'h' in tf:
            tfd = int(tf.replace('h', '')) * 60 * 60
        elif 'D' in tf:
            tfd = int(tf.replace('D', '')) * 60 * 60 * 24
        elif 'M' in tf:
            tfd = int(tf.replace('M', '')) * 60 * 60 * 24 * 30
        else:
            raise ValueError('Unknown timeframe {}! Exiting...'.format(tf))
        return tfd

    @staticmethod
    def candle_indexes():
        """Return indexes for candle list.
        @see https://docs.bitfinex.com/reference#rest-public-candles"""
        return ['MTS', 'OPEN', 'CLOSE', 'HIGH', 'LOW', 'VOLUME']

    @staticmethod
    def candle2dict(candle):
        return dict(zip(BitfinexHelper.candle_indexes(), candle))

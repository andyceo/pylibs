#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Bitfinex helper class (contain useful static methods and documentation)"""
from timeframeds import Timeframe


class BitfinexHelper:
    apiv2_description = {
        'rpe_candles': {
            'group': 'RPE',
            'method': 'GET',
            'endpoint': 'https://api-pub.bitfinex.com/v2/candles/trade:TimeFrame:Symbol/Section',
        }
    }
    """Structured Bitfinex API endpoints description based on https://docs.bitfinex.com/reference"""

    apiv2_groups = {
        'RPE': 'REST Public Endpoints',
        'RCE': 'REST Calculation Endpoints',
    }
    """Groups of Bitfinex API endpoints"""

    @staticmethod
    def tfd(tf: str) -> int:
        # @todo: refactor using tfd method
        return Timeframe.duration(tf)

    @staticmethod
    def candle_indexes():
        """Return indexes for candle list.
        @see https://docs.bitfinex.com/reference#rest-public-candles"""
        return ['MTS', 'OPEN', 'CLOSE', 'HIGH', 'LOW', 'VOLUME']

    @staticmethod
    def candle2dict(candle):
        return dict(zip(BitfinexHelper.candle_indexes(), candle))

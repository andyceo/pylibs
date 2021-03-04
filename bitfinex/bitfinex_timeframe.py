#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Bitfinex Timeframe class. Contain only timeframe that is allowed on Bitfinex"""
from timeframeds import Timeframe


class BitfinexTimeframe(Timeframe):
    """Timeframes allowed on Bitfinex"""
    def __init__(self, timeframe: str):
        self.timeframe = BitfinexTimeframe.change(timeframe)

    @staticmethod
    def change(timeframe):
        """Change timeframe to allowed timeframe code"""
        changes = {'1W': '7D'}
        return changes[timeframe] if timeframe in changes else timeframe

    @staticmethod
    def timeframes():
        """Return the tuple containing allowed timeframe codes"""
        return '1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1D', '7D', '14D', '1M'

    @staticmethod
    def is_allowed(timeframe: str):
        """Check if given timeframe is allowed"""
        return timeframe in BitfinexTimeframe.timeframes()

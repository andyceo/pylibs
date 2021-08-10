#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Bunch of date and time functions"""
import datetime
import time


def gmtdt(ts=time.time()) -> str:
    """Convert given timestamp into GMT ISO date string. Timestamp treated as UTC. If no timestamp given, use current"""
    return datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc).replace(microsecond=0).isoformat()


def mstimestamp(ts=0) -> int:
    """
    Return given timestamp as milliseconds timestamp, return current milliseconds timestamp otherwise
    (1 sec = 1000 ms)
    """
    ts = float(ts) if ts else time.time()
    return round(ts*1000)

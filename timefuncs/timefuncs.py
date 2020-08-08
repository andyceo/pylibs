#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Bunch of date and time functions"""
import datetime
import time


def gmtdt(ts=time.time()) -> str:
    """Convert given timestamp into GMT ISO date string. Timestamp treated as UTC. If no timestamp given, use current"""
    return datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc).replace(microsecond=0).isoformat()

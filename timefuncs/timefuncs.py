#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Bunch of date and time functions"""
import datetime


def gmtstr(ts: float) -> str:
    """Convert given timestamp into GMT ISO date string. Timestamp treated as UTC"""
    return datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc).replace(microsecond=0).isoformat()

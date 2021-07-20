#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Contain SQL model Log to represent table designed to store python logs (logging module)"""
from peewee import Model, CharField, TextField
from ..peeweext import UnsignedSmallIntegerField, UnsignedIntegerField, UnsignedBigIntegerField


class LogRecord(Model):
    """
    Represent a LogRecord storage.
    @see https://docs.python.org/3/library/logging.html#logrecord-attributes for reference
    """
    created = UnsignedIntegerField()
    filename = CharField(max_length=255)
    funcName = CharField(max_length=255)
    levelname = CharField(max_length=8)
    levelno = UnsignedSmallIntegerField()
    lineno = UnsignedIntegerField()
    message = TextField()
    module = CharField(max_length=255)
    msecs = UnsignedIntegerField()
    name = CharField(max_length=255)
    pathname = CharField(max_length=255)
    process = UnsignedIntegerField()
    processName = CharField(max_length=255)
    thread = UnsignedBigIntegerField()
    threadName = CharField(max_length=255)

    class Meta:
        table_name = 'log_record'

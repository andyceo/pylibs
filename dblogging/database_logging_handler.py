#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Contains DatabaseLoggingHandler class that can be used as handler with logging module to store log message to DB"""
import logging
from peewee import Database


class DatabaseLoggingHandler(logging.Handler):
    """Customized logging handler that puts logs to the database"""
    def __init__(self, database: Database, model):
        logging.Handler.__init__(self)
        database.bind([model])
        database.create_tables([model])
        self.model = model

    def emit(self, record):
        message = self.format(record)
        self.model.create(
            created=record.created,
            filename=record.filename,
            funcName=record.funcName,
            levelname=record.levelname,
            levelno=record.levelno,
            lineno=record.lineno,
            message=message,
            module=record.module,
            msecs=record.msecs,
            name=record.name,
            pathname=record.pathname,
            process=record.process,
            processName=record.processName,
            thread=record.thread,
            threadName=record.threadName
        )

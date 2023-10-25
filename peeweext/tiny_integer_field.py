#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Contains TinyIntegerField class"""
from peewee import IntegerField


class TinyIntegerField(IntegerField):
    """Represents tiny integer field"""
    field_type = 'TINYINT'

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Contains UnsignedSmallIntegerField class"""
from peewee import SmallIntegerField


class UnsignedSmallIntegerField(SmallIntegerField):
    """Represents unsigned small integer field"""
    field_type = 'SMALLINT UNSIGNED'

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Contains UnsignedTinyIntegerField class"""
from peewee import IntegerField


class UnsignedTinyIntegerField(IntegerField):
    """Represents unsigned tiny integer field"""
    field_type = 'TINYINT UNSIGNED'

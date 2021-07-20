#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Contains UnsignedBigIntegerField class"""
from peewee import BigIntegerField


class UnsignedBigIntegerField(BigIntegerField):
    """Represents unsigned big integer field"""
    field_type = 'BIGINT UNSIGNED'

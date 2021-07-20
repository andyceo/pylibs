#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Contains UnsignedIntegerField class"""
from peewee import IntegerField


class UnsignedIntegerField(IntegerField):
    """Represents unsigned integer field"""
    field_type = 'INT UNSIGNED'

# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file contains a metaclass Singleton that should be used in singleton classes.
Examples:

    class Logger(metaclass=Singleton):
        pass

If you want to run __init__ every time the class is called, add

    else:
        cls._instances[cls].__init__(*args, **kwargs)

to the if statement in Singleton.__call__.

@see https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python"""


class Singleton(type):
    """Minimalistic Singleton pattern implementation. Use this class as parent for classes that mean to be Singletons"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

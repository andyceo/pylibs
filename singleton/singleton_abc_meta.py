# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file contains a metaclass SingletonABCMeta that should be used in abstract singleton classes.
Examples:

    class Logger(metaclass=SingletonABCMeta):
        pass

If you want to run __init__ every time the class is called, add

    else:
        cls._instances[cls].__init__(*args, **kwargs)

to the if statement in SingletonABCMeta.__call__.

@see https://stackoverflow.com/questions/33364070/implementing-singleton-as-metaclass-but-for-abstract-classes
"""
from abc import ABCMeta


class SingletonABCMeta(ABCMeta):
    """Minimalistic abstract Singleton pattern implementation.
    Use this class as parent for classes that mean to be abstract Singletons"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonABCMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

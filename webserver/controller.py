#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Implements basic controller with reference to BaseHTTPServer so that it can access the web request
and write out the response.
@see http://aventures-logicielles.blogspot.com/2011/04/very-simple-http-server-with-basic-mvc.html"""


class Controller(object):

    def __init__(self, server):
        self.__server = server

    @property
    def server(self):
        return self.__server

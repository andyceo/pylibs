#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Implements basic controller with reference to BaseHTTPServer so that it can access the web request
and write out the response.
@see http://aventures-logicielles.blogspot.com/2011/04/very-simple-http-server-with-basic-mvc.html"""


class Controller(object):

    def __init__(self, server):
        self.__server = server

    def helloWorldExample(self):
        """Example for Hello World controller"""
        self.server.sendrsp(content='Hello world')

    def helloWorldAlternativeExample(self):
        """Alternative example for Hello World controller (manual control)"""
        self.server.send_response(200)
        self.server.send_header('Content-type', 'text/plain')
        self.server.end_headers()
        self.server.wfile.write()

    @property
    def server(self):
        return self.__server

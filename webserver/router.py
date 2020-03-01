#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Implements basic router.

@see http://aventures-logicielles.blogspot.com/2011/04/very-simple-http-server-with-basic-mvc.html

Usage example:

class MyWebServer(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):

        routes = [
            {'regexp': r'^/$', 'module': '__main__', 'controller': 'HomeController', 'action': 'indexAction'},
            {'regexp': r'^/content/', 'module': '__main__', 'controller': 'ContentController', 'action': 'showAction'}
        ]

        self.__router = Router(self)
        for route in routes:
            self.__router.addRoute(route['regexp'], route['controller'], route['action'])

        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        self.__router.route(self.path)
"""
import re
import sys


class Router(object):

    def __init__(self, server):
        self.__routes = []
        self.__server = server

    def addRoute(self, regexp, module, controller, action):
        self.__routes.append({'regexp': regexp, 'module': module, 'controller': controller, 'action': action})

    def route(self, path):
        for route in self.__routes:
            if re.search(route['regexp'], path):
                cls = getattr(sys.modules[route['module']], route['controller'])
                func = cls.__dict__[route['action']]
                obj = cls(self.__server)
                func(obj)
                return

        # Not found
        self.__server.send_response(404)
        self.__server.end_headers()

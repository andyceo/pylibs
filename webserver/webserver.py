#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Implements basic web server with some default GET requests handling and logging"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
import sys


class WebServer(BaseHTTPRequestHandler):
    def _send_rsp(self, code=200, headers=None, content='Hello World!', encoding='utf8'):
        # Calculate content and Content-type header
        cth = ('Content-type', 'text/plain')
        if isinstance(content, (dict, set, list, tuple)):
            content = json.dumps(content, sort_keys=True, indent=4)
            cth = ('Content-type', 'application/json')
        elif not isinstance(content, str):
            content = "Error: unknown content type of '{}' given into _send_response() function!"\
                .format(type(content).__name__)
            code = 500

        # Send response status code
        self.send_response(code)

        # Send headers
        if not headers:
            headers = [cth]
        for header in headers:
            self.send_header(*header)
        self.end_headers()

        # Write content as encoded data with given encoding
        self.wfile.write(content.encode(encoding))

    def do_GET(self):
        logging.info("Received GET query: '%s'", self.path)
        self._send_rsp()
        sys.stdout.flush()  # for printing log messages immediately


def run(bind_address='0.0.0.0', port=8080):
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(module)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info('Starting httpd...\n')
    server_address = (bind_address, port)
    httpd = HTTPServer(server_address, WebServer)
    logging.info('Running httpd...\n')
    sys.stdout.flush()  # for printing log messages immediately
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info('Keyboard interrupt, finishing httpd...\n')
    httpd.server_close()
    logging.info('httpd stopped.\n')


if __name__ == '__main__':
    run()
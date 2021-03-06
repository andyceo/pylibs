#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Implements basic web server with some default GET requests handling and logging"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime
import json
import logging
import sys


class WebServer(BaseHTTPRequestHandler):
    def _send_rsp(self, code=200, headers=None, content='Hello World!', encoding='utf8', start_ts=0):
        # Calculate content and Content-type header
        cth = ('Content-type', 'text/plain')
        if isinstance(content, (dict, set, list, tuple)):
            if start_ts:  # Add request timing info if start_ts not zero
                content['request_timing'] = {
                    'received_timestamp': start_ts,
                    'received_date': datetime.datetime.fromtimestamp(start_ts, tz=datetime.timezone.utc).replace(
                        microsecond=0).isoformat(),
                    'executed_time': datetime.datetime.now().timestamp() - start_ts,
                }
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

        sys.stdout.flush()  # for printing log messages immediately

    def sendrsp(self, code=200, headers=None, content='Hello World!', encoding='utf8', start_ts=0):
        """Send response to client"""
        self._send_rsp(code=code, headers=headers, content=content, encoding=encoding, start_ts=start_ts)

    def do_GET(self):
        """Default handler for all GET requests"""
        self._send_rsp()


def run_webserver(bind_address='0.0.0.0', port=8080, logger=None,
                  webserver_class='WebServer', webserver_class_module=__name__):
    if not logger:
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] %(levelname)s [%(name)s.%(module)s.%(funcName)s:%(lineno)d] %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        logger = logging.getLogger()

    logger.info('Starting httpd...')
    server_address = (bind_address, port)
    httpd = HTTPServer(server_address, getattr(sys.modules[webserver_class_module], webserver_class))
    logger.info('Running httpd...')
    sys.stdout.flush()  # for printing log messages immediately
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info('Keyboard interrupt, finishing httpd...')
    httpd.server_close()
    logger.info('httpd stopped.')


if __name__ == '__main__':
    run_webserver()

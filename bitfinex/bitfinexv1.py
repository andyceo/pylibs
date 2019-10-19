#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Store BitfinexV1 class"""
import base64
import hashlib
import hmac
import json
import requests
import time


class ApiError(requests.exceptions.HTTPError):
    pass


class ApiErrorRateLimit(ApiError):
    pass


class BitfinexV1(object):
    """Allow make queries to Bitfinex API v1 (stable). See https://docs.bitfinex.com/v1/docs"""
    api_key = ''
    api_secret = ''
    api_url = 'https://api.bitfinex.com'
    timeout = 5.0

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def account_infos(self):
        """Return information about your account (trading fees) (POST, auth, rate limit: 5)
            Documentation: https://docs.bitfinex.com/v1/reference#rest-auth-account-info
        """
        data = {'request': self.endpoint('account_infos')}
        return self.send_auth_request(data)

    def account_fees(self):
        """See the fees applied to your withdrawals (POST, auth, rate limit: 5)
            Documentation: https://docs.bitfinex.com/v1/reference#rest-auth-fees
        """
        data = {'request': self.endpoint('account_fees')}
        return self.send_auth_request(data)

    def cancel_offer(self, offer_id):
        """Cancel the offer."""
        data = {
            'request': self.endpoint('offer', 'cancel'),
            'offer_id': offer_id
        }
        return self.send_auth_request(data)

    def get_balances(self):
        request = self.endpoint('balances')
        data = {'request': request}
        return self.send_auth_request(data)

    def get_offers(self):
        """View your active offers (POST, auth, rate limit: unknown).
            Documentation: https://docs.bitfinex.com/v1/reference#rest-auth-offers
        """
        data = {'request': self.endpoint('offers')}
        return self.send_auth_request(data)

    def get_offers_hist(self, limit=None):
        """View your latest inactive offers. Limited to last 3 days and 1 request per minute
        (POST, auth, rate limit: 1)
        """
        data = {'request': self.endpoint('offers', 'hist')}
        if limit:
            data['limit'] = limit
        return self.send_auth_request(data)

    def get_history_movements(self, currency='usd', method='bitcoin', limit=500, since=None, until=None):
        """View your past deposits/withdrawals."""
        data = {
            'request': self.endpoint('history', 'movements'),
            'currency': currency,
            'method': method,
            'limit': limit
        }
        if since:
            data['since'] = since
        if until:
            data['until'] = until
        return self.send_auth_request(data)

    def new_offer(self, currency, amount, rate, period, direction='lend'):
        """Submit a new offer."""
        request = self.endpoint('offer', 'new')
        data = {
            'request': request,
            'currency': currency,
            'amount': amount,
            'rate': rate,
            'period': period,
            'direction': direction
        }
        return self.send_auth_request(data)

    def get_lendbook(self, currency='usd', data={}):
        """Get the full margin funding book."""
        request = self.endpoint('lendbook', currency)
        return self.send_public_request(request, data)

    def get_orderbook(self, symbol='btcusd', data={}):
        """Get the full order book (GET, no auth, rate limit: 30)
            Documentation: https://docs.bitfinex.com/v1/reference#rest-public-orderbook
        """
        request = self.endpoint('book', symbol)
        return self.send_public_request(request, data)

    def get_symbols(self):
        """A list of symbol names (GET, no auth, rate limit: 10)
            Documentation: https://docs.bitfinex.com/v1/reference#rest-public-symbols
        """
        request = self.endpoint('symbols')
        return self.send_public_request(request)

    def get_ticker(self, symbol='btcusd'):
        """
        Gives innermost bid and asks and information on the most recent trade, as
        well as high, low and volume of the last 24 hours (GET, no auth, rate limit: 20)
            Documentation: https://docs.bitfinex.com/v1/reference#rest-public-ticker
        """
        request = self.endpoint('pubticker', symbol)
        return self.send_public_request(request)

    # Method aliases for better experience
    funding_book = get_lendbook

    @staticmethod
    def endpoint(method, params=None):
        """Construct an endpoint URL"""
        if params is not None:
            if isinstance(params, str):
                parameters = '/' + params
            else:
                parameters = '/' + '/'.join(params)
        else:
            parameters = ''
        return "/v1/" + method + parameters

    def send_public_request(self, request, params=None):
        """Send an unsigned HTTP request"""
        url = self.api_url + request
        response = requests.get(url, timeout=self.timeout, params=params)
        return self._response_error_handling(response)

    def send_auth_request(self, data):
        """"Send a signed HTTP request"""
        url = self.api_url + data['request']
        headers = self.prepare_header(data)
        response = requests.post(url, headers=headers, timeout=self.timeout)
        return self._response_error_handling(response)

    @staticmethod
    def _response_error_handling(response):
        result = response.json()
        if response.status_code != 200:
            result['status_code'] = response.status_code
            if 'error' in result:
                if result['error'] == 'ERR_RATE_LIMIT':
                    raise ApiErrorRateLimit(json.dumps(result))
            raise ApiError(json.dumps(result))
        return result

    def prepare_header(self, data):
        """Add data to header for authentication purpose"""
        data['nonce'] = "{0:d}".format(round(time.time() * 100000))
        payload = base64.b64encode(json.dumps(data, separators=(',', ':')).encode())
        signature = hmac.new(bytes(self.api_secret, "utf-8"), payload, hashlib.sha384).hexdigest()
        return {
            'X-BFX-APIKEY': self.api_key,
            'X-BFX-PAYLOAD': payload,
            'X-BFX-SIGNATURE': signature
        }

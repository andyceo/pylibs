import base64
import hashlib
import hmac
import json
import requests
import time


class BitfinexV1(object):

    api_key = ''
    api_secret = ''
    api_url = 'https://api.bitfinex.com'
    timeout = 5.0

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

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
        """View your active offers."""
        data = {'request': self.endpoint('offers')}
        return self.send_auth_request(data)

    def get_offers_hist(self):
        """View your active offers."""
        # @todo: add support for limit param.
        data = {'request': self.endpoint('offers', 'hist')}
        return self.send_auth_request(data)

    def get_history_movements(self, currency='usd', method='bitcoin', limit=500, since=None, until=None):
        """View your past deposits/withdrawals."""
        request = self.endpoint('history', 'movements')
        data = {
            'request': request,
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
        """Get the full order book."""
        request = self.endpoint('book', symbol)
        return self.send_public_request(request, data)

    def get_symbols(self):
        """Get a list of valid symbol IDs."""
        request = self.endpoint('symbols')
        return self.send_public_request(request)

    def get_ticker(self, symbol='btcusd'):
        """
        Gives innermost bid and asks and information on the most recent trade, as
        well as high, low and volume of the last 24 hours.
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
        # @todo: process API errors
        return requests.get(url, timeout=self.timeout, params=params).json()

    def send_auth_request(self, data):
        """"Send a signed HTTP request"""
        url = self.api_url + data['request']
        headers = self.prepare_header(data)
        # @todo: process API errors
        return requests.post(url, headers=headers, timeout=self.timeout).json()

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

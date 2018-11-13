import requests


class BitcoinChainSoApi():
    def __init__(self):
        self._baseurl = 'https://chain.so'
        self._timeout = 5

    def request(self, uri):
        return requests.get(self._baseurl + uri, timeout=self._timeout).json()


class CryptoBalance():
    def __init__(self, network, address=None):
        self._network = network
        self._address = address
        self._provider = BitcoinChainSoApi()

    def get_balance(self, address=None, confirmations=10):
        if address is None:
            if self._address is None:
                return None
            else:
                address = self._address
        return self._provider.request('/api/v2/get_address_balance/BTC/{}/{}'.format(
            address, confirmations
        ))


if __name__ == "__main__":
    address = '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'  # The Genesis Address
    cb = CryptoBalance('btc')
    print(cb.get_balance(address))

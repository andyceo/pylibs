#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Show how many BTC you must send to recipient to allow him exchange that BTC to given russian ruble amount,
with current exchange rates."""

import argparse
import requests

BINANCE_BTCUSDT_URL = 'https://api.binance.com/api/v1/ticker/price?symbol=BTCUSDT'
CBRF = 'https://www.cbr-xml-daily.ru/daily_json.js'
COMISSION = 0.03  # 3%

if __name__ == '__main__':
    req = requests.get(BINANCE_BTCUSDT_URL, timeout=5)
    btcusdt = float(req.json()['price'])

    req = requests.get(CBRF, timeout=5)
    usdrub = float(req.json()['Valute']['USD']['Value'])

    print('BTC/USD:', btcusdt)
    print('USD/RUB:', usdrub)
    print('BTC/RUB:', btcusdt * usdrub)

    c = 1 - COMISSION

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('amounts', metavar='N', type=int, nargs='+', help='Amounts to calculate')
    args = parser.parse_args()

    for amount in args.amounts:
        res = amount / btcusdt / usdrub / c
        print('{} / {} / {} / {} = {}'.format(amount, btcusdt, usdrub, c, res))

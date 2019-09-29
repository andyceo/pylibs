#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Show how many BTC you must send to recipient to allow him exchange that BTC to given russian ruble amount,
with current exchange rates."""

import argparse
import os
import requests


def btcusdt():
    req = requests.get('https://api.binance.com/api/v1/ticker/price?symbol=BTCUSDT', timeout=5)
    return float(req.json()['price'])


def usdrub():
    req = requests.get('https://www.cbr-xml-daily.ru/daily_json.js', timeout=5)
    return float(req.json()['Valute']['USD']['Value'])


def btcrub(btcusd, usdrub):
    return round(btcusd * usdrub, 2)


def btcamount(rubamount, btcusd, usdrub, fee):
    return rubamount / btcusd / usdrub / (1-fee/100)


if __name__ == '__main__':
    btcusdt = btcusdt()
    usdrub = usdrub()

    print('BTC/USD:', btcusdt)
    print('USD/RUB:', usdrub)
    print('BTC/RUB:', btcrub(btcusdt, usdrub))

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('amounts', metavar='N', type=int, nargs='+', help='Amounts to calculate')
    parser.add_argument('--fee', metavar='FEE', default=os.environ.get('FEE', 3), help='Fee, in percent')
    args = parser.parse_args()
    c = 1-args.fee/100

    for amount in args.amounts:
        res = btcamount(amount, btcusdt, usdrub, args.fee)
        print('{} / {} / {} / {} = {}'.format(amount, btcusdt, usdrub, c, res))

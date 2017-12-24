import datetime


def message(msg):
    date = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
    print("{0:s} {1:s}".format(date, msg))


def timestamp_useless_microseconds(ts):
    if type(ts) is str and ts[-2:] == ".0":
        return True
    return False


def timestamp2int(ts):
    if type(ts) is str:
        ts = float(ts)
    # int() is for python2 version (where round always return float)
    return int(round(ts))


def timestamp_normalize(ts):
    if timestamp_useless_microseconds(ts):
        return timestamp2int(ts)
    else:
        return ts


def normalize_offers(offers):
    if 'message' in offers:
        message('API Error: {}'.format(offers['message']))
        exit(1)
    for offer in offers:
        offer['timestamp'] = timestamp_normalize(offer['timestamp'])
    return offers


def normalize_dict(d):
    if 'timestamp' in d:
        d['timestamp'] = timestamp_normalize(d['timestamp'])
    if 'amount' in d:
        d['amount'] = int(d['amount']) if d['amount'].find('.') == -1 else float(d['amount'])
    if 'price' in d:
        d['price'] = int(d['price']) if d['price'].find('.') == -1 else float(d['price'])
    return d


def bfxv1_private_balances(bfx):
    balances = bfx.get_balances()
    for balance in balances:
        balance['amount'] = float(balance['amount'])
        balance['available'] = float(balance['available'])
    return balances


def bfxv1_private_offers(bfx):
    offers = bfx.get_offers()
    return normalize_offers(offers)


def bfxv1_private_offers_hist(bfx):
    offers_hist = bfx.get_offers_hist()
    return normalize_offers(offers_hist)


if __name__ == '__main__':
    test = [12345678, 1234567.8, "1234567.8", "1234567.2", "1234567.0", "12345678"]
    for t in test:
        transformed = timestamp2int(t)
        print(t, '->', transformed, ', ', type(t), '->', type(transformed))

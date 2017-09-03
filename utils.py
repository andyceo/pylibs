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


def bfx_private_offers_hist(bfx):
    offers_hist = bfx.get_offers_hist()
    if 'message' in offers_hist:
        message('API Error: {}'.format(offers_hist['message']))
        exit(1)
    for offer in offers_hist:
        offer['timestamp'] = timestamp_normalize(offer['timestamp'])
    return offers_hist

if __name__ == '__main__':
    test = [12345678, 1234567.8, "1234567.8", "1234567.2", "1234567.0", "12345678"]
    for t in test:
        transformed = timestamp2int(t)
        print(t, '->', transformed, ', ', type(t), '->', type(transformed))

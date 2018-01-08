#!/usr/bin/env python3

import copy
import calendar
import datetime
import os
import shutil
import sys
import tarfile
import time


def message(msg):
    date = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
    print("{0:s}Z {1:s}".format(date, msg))
    sys.stdout.flush()


def isodatestring2timestamp(s):
    struct_time = time.strptime(s, '%Y-%m-%dT%H:%M:%SZ')
    return int(calendar.timegm(struct_time))


def timestamp_useless_microseconds(ts):
    if type(ts) is str and ts[-2:] == ".0":
        return True
    return False


def timestamp2int(ts):
    if type(ts) is str:
        ts = float(ts)
    return round(ts)


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


def normalize_number(n):
    if type(n) is str:
        if n.find('.') == -1 and n.find('e') == -1:
            n = int(n)
        else:
            n = float(n)
    elif type(n) is not float and n is not int:
        n = 0
    return n


def normalize_dict(dictionary):
    d = copy.deepcopy(dictionary)
    if 'timestamp' in d:
        d['timestamp'] = timestamp_normalize(d['timestamp'])
    if 'amount' in d:
        d['amount'] = normalize_number(d['amount'])
    if 'price' in d:
        d['price'] = normalize_number(d['price'])
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


def archive_directory(archive_filename, source_dir, mode='w:gz'):
    if mode == 'w:xz':
        # Using undocumented preset parameter for tarfile.open for lzma compression to maximize compression level for
        # xz formats. It was found reading lzma module documentation for lzma.open() function.
        with tarfile.open(archive_filename, mode, preset=9) as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))
    else:
        with tarfile.open(archive_filename, mode, compresslevel=9) as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))


def archive_directory_safe(output_filename, source_dir, mode='w:gz'):
    if os.path.isdir(source_dir):
        dirsize = sum(os.path.getsize(f) for f in os.listdir(source_dir) if os.path.isfile(f))
        statvfs = os.statvfs(source_dir)
        freespace = statvfs.f_frsize * statvfs.f_bavail
        if dirsize + 1024 > freespace:
            message("Free space {} may not be enough for archiving! Exiting...".format(freespace))
            return False

        archive_directory(output_filename, source_dir, mode)

        if not test_archive(output_filename):
            message("Something goes wrong checking archive. Exiting...")
            return False

        shutil.rmtree(source_dir)
        return True

    return False


def test_archive(archive_filename):
    try:
        tardude = tarfile.open(archive_filename)
    except:
        message("There was an error opening tarfile. The file might be corrupt or missing.")
        return False

    try:
        members = tardude.getmembers()
    except:
        message("There was an error reading tarfile members.")
        return False

    for member in members:
        if member.isfile():
            try:
                with tardude.extractfile(member.name) as target:
                    for chunk in iter(lambda: target.read(1024), b''):
                        pass
            except:
                message("File: {} is corrupt.".format(member.name))
                return False

    return True


if __name__ == '__main__':
    test = [12345678, 1234567.8, "1234567.8", "1234567.2", "1234567.0", "12345678"]
    for t in test:
        transformed = timestamp2int(t)
        print(t, '->', transformed, ', ', type(t), '->', type(transformed))

    test = [
        {'input': '2017-12-25T14:59:21Z', 'output': 1514213961}
    ]
    for t in test:
        transformed = isodatestring2timestamp(t['input'])
        is_ok = 'OK' if transformed == t['output'] else 'FAIL'
        is_eq = '==' if transformed == t['output'] else '!='
        print("{}: {}({}) -> {}({}) {} {}".format(is_ok, t['input'], type(t['input']), transformed, type(transformed),
                                                  is_eq, t['output']))

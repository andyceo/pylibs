#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""HistoryDataset visualizing with mplfinance, matplotlib and pandas"""
import calendar
from pprint import pprint
import ciso8601
import mplfinance as mpf
import pandas as pd
from timeframeds import TimeframeDataset


def tfds2pdf(tfds: TimeframeDataset):
    """Convert given TimeframeDataset tfds to Pandas Dataframe"""
    d = {}
    for i, _ in enumerate(tfds):
        drow = tfds.get_dict(i, timestamp_format='human')
        dt = drow[tfds.tsname]
        del drow[tfds.tsname]
        d[dt] = drow
    pdf = pd.DataFrame.from_dict(d, orient='index')
    pdf.index.name = tfds.tsname
    pdf.index = pd.to_datetime(pdf.index)
    return pdf


def plot(tfds: TimeframeDataset):
    """Plot given TimeframeDataset tfds"""
    mpf.plot(tfds2pdf(tfds), type='candle', show_nontrading=True)


if __name__ == '__main__':
    print('Welcome to TimeframeDataset plotter!')
    print()

    # Define the example data
    t = {
        'data': [
            ('2020.07.20 15:30', 9187.6, 9192.9, 9187.6, 9192.8),
            ('2020.07.20 16:00', 9192.8, 9192.8, 9189.8, 9189.8),
            ('2020.07.20 16:30', 9189.8, 9189.8, 9183.9, 9187.0),
            ('2020.07.20 17:00', 9187.0, 9208.2, 9187.0, 9208.1),
            ('2020.07.20 17:30', 9208.1, 9217.1, 9208.1, 9213.6),
            ('2020.07.20 18:00', 9213.6, 9216.1, 9200.0, 9201.7),
            ('2020.07.20 18:30', 9201.6, 9201.7, 9197.1, 9197.1),
            ('2020.07.20 19:00', 9197.2, 9199.9, 9193.0, 9193.9),
            ('2020.07.20 19:30', 9193.8, 9193.8, 9164.3, 9173.7),
            ('2020.07.20 20:00', 9174.2, 9194.2, 9173.9, 9194.2),
            ('2020.07.20 20:30', 9194.2, 9197.9, 9180.3, 9189.5),
            ('2020.07.20 21:00', 9189.5, 9189.5, 9169.8, 9179.0),
        ],
        'columns': ['Datetime', 'Open', 'High', 'Low', 'Close'],
        'tsname': 'Datetime',
        'timeframe': '30m',
        'tsunit': 's',
        'tscoef': 1,
        'tsindex': 2
    }

    # Convert datetime sting to timestamps before creating TimeframeDataset
    for index, item in enumerate(t['data']):
        item = list(item)
        newdatestr = item[0].replace('.', '-').replace(' ', 'T')
        item[0] = calendar.timegm(ciso8601.parse_datetime_as_naive(newdatestr).timetuple())
        t['data'][index] = item

    # Create the TimeframeDataset and print it
    tfds = TimeframeDataset(data=t['data'], columns=t['columns'], tsname=t['tsname'], timeframe=t['timeframe'],
                                  tsunit=t['tsunit'])
    pprint(tfds)
    print()

    # Create Pandas Dataframe from TimeframeDataset and print it
    pdf = tfds2pdf(tfds)
    print(pdf)
    print()

    # Plot TimeframeDataset via mplfinance
    plot(tfds)

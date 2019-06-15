import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_finance import candlestick_ohlc, volume_overlay3
import matplotlib.dates as dates
import datetime
import matplotlib.transforms as transform
import re


def _request(morepayload):
    # QUERY_URL = "https://www.alphavantage.co/query?function={REQUEST_TYPE}&apikey={KEY}&symbol={SYMBOL}&datatype=json"

    QUERY_URL = "https://www.alphavantage.co/query?"

    API_KEY = '32LEG0B1PYUNA7WO'

    payload = {'apikey': '32LEG0B1PYUNA7WO', 'datatype': 'json'}
    payload.update(morepayload)

    # data = requests.get(QUERY_URL.format(
    #    REQUEST_TYPE=req_type, KEY=API_KEY, SYMBOL=symbol))

    data = requests.get(QUERY_URL, params=payload)
    return data.json()


def get_daily_data(symbol):
    return _request({'symbol': symbol,
                     'function': 'TIME_SERIES_DAILY',
                     'outputsize': 'full'})


def get_RSI(symbol, days):
    return _request({'symbol': symbol,
                     'function': 'RSI',
                     'series_type': 'close',
                     'time_period': days,
                     'interval': 'daily'
                     })


def get_MACD(symbol):
    return _request({'symbol': symbol,
                     'function': 'MACD',
                     'series_type': 'close',
                     'interval': 'daily'
                     })


def write_this(data, symbol):

    info = str(list(data.keys())[1]).replace(":", "", 3)

    with open(symbol + '_' + info + '.txt', 'w') as outfile:
        json.dump(data, outfile)


def overlay_volume(ax1, data_df):
    ax2 = ax1.twinx()

    # make bar plots and color differently depending on up/down for the day
    pos = data_df['1. open']-data_df['4. close'] <= 0
    neg = data_df['1. open']-data_df['4. close'] > 0
    ax2.bar(data_df['index'][pos].values, data_df['5. volume'][pos],
            color='green', width=1, align='center', alpha=0.3)
    ax2.bar(data_df['index'][neg].values, data_df['5. volume'][neg],
            color='red', width=1, align='center', alpha=0.3)

    yticks = ax2.get_yticks()

    ax2.yaxis.set_label_position("right")
    ax2.set_ylim([0, 5*data_df['5. volume'].max()])
    ax2.set_yticks(
        np.arange(0, data_df['5. volume'].max()*1.25+1, data_df['5. volume'].max()/4))

    return ax2


def overlay_ema(ax, dates, prices, days):
    exp = prices.ewm(span=days, adjust=False).mean()

    legend = '{SPAN} Day EMA'.format(SPAN=days)
    return ax.plot(dates, exp, label=legend)


# data = get_daily_data('FB')
# write_this(data, 'FB')

# data_RSI = get_RSI('FB', 28)
# write_this(data_RSI, 'FB')

# data_MACD = get_MACD('FB')
# write_this(data_MACD, 'FB')


# with open('FB_Time Series (Daily).txt') as json_file:
with open('output.txt') as json_file:
    data = json.load(json_file)
    time_series = data['Time Series (Daily)']
    data_df = pd.DataFrame(time_series).transpose()
    data_df = data_df.astype(float)
    data_df.reset_index(level=0, inplace=True)
    data_df['index'] = dates.date2num(list(map(datetime.datetime.strptime,
                                               data_df['index'], len(data_df['index'])*['%Y-%m-%d'])))
    data_df.sort_values(by=['index'], inplace=True)


# add subplot
f1, ax1 = plt.subplots(figsize=(10, 5))

# plot the candlesticks,
candlestick_ohlc(ax1, data_df.values, width=0.6,
                 colorup='green', colordown='red')

# grid settings
plt.grid(linestyle=':', linewidth='0.5', color='black')

# axis settings
plt.xticks(rotation=90)
ax1.xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
ax1.xaxis.set_major_locator(
    dates.WeekdayLocator(byweekday=dates.MO)
)
ax1.xaxis.set_major_formatter(
    dates.DateFormatter('%Y-%m-%d')
)
ax1.set_ylabel('Price')

# add volume plot
overlay_volume(ax1, data_df)

# add EMA plots
overlay_ema(ax1, data_df['index'], data_df['4. close'], 10)

overlay_ema(ax1, data_df['index'], data_df['4. close'], 20)
ax1.legend(loc='upper left')
plt.show()

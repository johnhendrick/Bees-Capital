import requests
import json
import requests
import matplotlib.pyplot as plt
import pandas as pd
from mpl_finance import candlestick_ohlc
import matplotlib.dates as dates


def _request(symbol, req_type):
    QUERY_URL = "https://www.alphavantage.co/query?function={REQUEST_TYPE}&apikey={KEY}&symbol={SYMBOL}&datatype=json"
    API_KEY = '32LEG0B1PYUNA7WO'

    data = requests.get(QUERY_URL.format(
        REQUEST_TYPE=req_type, KEY=API_KEY, SYMBOL=symbol))
    return data.json()


def get_daily_data(symbol):
    return _request(symbol, 'TIME_SERIES_DAILY')


def write_this(data):
    with open('output.txt', 'w') as outfile:
        json.dump(data, outfile)


# data = get_daily_data('MSFT')
# write_this(data)

with open('output.txt') as json_file:
    data = json.load(json_file)
    time_series = data['Time Series (Daily)']
    data_df = pd.DataFrame(time_series).transpose()
    data_df = data_df.astype(float)


# print(type(time_series))
# print(data_df.index.values)
df_plot = data_df[['1. open', '2. high', '3. low', '4. close']]

# f1, ax = plt.subplots(figsize=(10, 5))

# # plot the candlesticks
# candlestick_ohlc(ax, df_plot, width=0.6, colorup='green', colordown='red')

# plt.show()

print(df_plot.head())
print(df_plot.dtypes)

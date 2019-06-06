import requests
import json
import urllib.request

QUERY_URL = "https://www.alphavantage.co/query?function={REQUEST_TYPE}&apikey={KEY}&symbol={SYMBOL}"
API_KEY = '32LEG0B1PYUNA7WO'

def _request(symbol, req_type):
    with urllib.request.urlopen(QUERY_URL.format(REQUEST_TYPE=req_type, KEY=API_KEY, SYMBOL=symbol)) as req:
        data = req.read().decode("UTF-8")
    return data

def get_daily_data(symbol):
    return json.loads(_request(symbol, 'TIME_SERIES_DAILY'))

def write_this(data):
    with open('output.txt', 'a') as outfile:  
        json.dump(data, outfile)
    
#write_this(data)
#data = get_daily_data('MSFT')

with open('output.txt') as json_file:  
    data = json.load(json_file)
    time_series= data['Time Series (Daily)']
    print(time_series['2019-06-06'])
       
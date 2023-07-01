# -*- coding: utf-8 -*-
"""
Alpaca API - Finding top movers using streaming V2 API

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""


import websocket
import os
import json
from alpaca_trade_api.rest import REST, TimeFrame
import threading
import time

os.chdir("D:\\OneDrive\\Alpaca") #change this based on the path on your local machine

endpoint = "https://data.alpaca.markets/v2"
headers = json.loads(open("key.txt",'r').read())
tickers = ['FB','AMZN','INTC','MSFT','AAPL','GOOG','CSCO','CMCSA','ADBE',
           'NVDA','NFLX','PYPL','AMGN','AVGO','TXN','CHTR','QCOM','GILD',
           'FISV','BKNG','INTU','ADP','CME','TMUS','MU']
ltp = {}
prev_close = {}
perc_change = {}

def hist_data(symbols, start_date ="2021-12-01", timeframe="Minute"):
    """
    returns historical bar data for a list of tickers e.g. symbols = ["MSFT,AMZN,GOOG"]
    """
    df_data = {}
    api = REST(headers["APCA-API-KEY-ID"], headers["APCA-API-SECRET-KEY"], base_url=endpoint)
    for ticker in symbols:
        if timeframe == "Minute":
            df_data[ticker] = api.get_bars(ticker, TimeFrame.Minute, start_date, adjustment='all').df
        elif timeframe == "Hour":
            df_data[ticker] = api.get_bars(ticker, TimeFrame.Hour, start_date, adjustment='all').df
        else:
            df_data[ticker] = api.get_bars(ticker, TimeFrame.Day, start_date, adjustment='all').df
    return df_data

    
data_dump = hist_data(tickers, timeframe="Day")
for ticker in tickers:
    prev_close[ticker] = data_dump[ticker]["close"][-2]
    ltp[ticker] = data_dump[ticker]["close"][-1]
    perc_change[ticker] = 0

def on_open(ws):
    auth = {"action": "auth", "key": headers["APCA-API-KEY-ID"], "secret": headers["APCA-API-SECRET-KEY"]}
    
    ws.send(json.dumps(auth))
    
    message = {"action":"subscribe","trades":tickers}
                
    ws.send(json.dumps(message))
 
def on_message(ws, message):
    #print(message)
    tick = json.loads(message)
    tkr = tick[0]["S"]
    ltp[tkr] = float(tick[0]["p"])
    perc_change[tkr] = round((ltp[tkr]/prev_close[tkr] - 1)*100,2)   
    

def connect():
    ws = websocket.WebSocketApp("wss://stream.data.alpaca.markets/v2/iex", on_open=on_open, on_message=on_message)
    ws.run_forever()


con_thread = threading.Thread(target=connect)
con_thread.start()

starttime = time.time()
timeout = starttime + 60*5
while time.time() <= timeout:
    for ticker in tickers:
        print("percent change for {} = {}".format(ticker,perc_change[ticker]))
    time.sleep(60 - ((time.time() - starttime) % 60))
    


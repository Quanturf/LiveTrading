# -*- coding: utf-8 -*-
"""
Alpaca API - MACD + stochastic strategy (V2 API)

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

import os
import json
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST, TimeFrame
import time

os.chdir("D:\\OneDrive\\Alpaca") #change this based on the path on your local machine

endpoint = "https://data.alpaca.markets/v2"
headers = json.loads(open("key.txt",'r').read())
api = tradeapi.REST(headers["APCA-API-KEY-ID"], headers["APCA-API-SECRET-KEY"], base_url='https://paper-api.alpaca.markets')
tickers = ['FB','AMZN','INTC','MSFT','AAPL','GOOG','CSCO','CMCSA','ADBE',
           'NVDA','NFLX','PYPL','AMGN','AVGO','TXN','CHTR','QCOM','GILD',
           'FISV','BKNG','INTU','ADP','CME','TMUS','MU']
max_pos = 3000 #max position size for each ticker
stoch_signal = {}
for ticker in tickers:
    stoch_signal[ticker] = ""

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

def MACD(df_dict, a=12 ,b=26, c=9):
    """function to calculate MACD
       typical values a(fast moving average) = 12; 
                      b(slow moving average) =26; 
                      c(signal line ma window) =9"""
    for df in df_dict:
        df_dict[df]["ma_fast"] = df_dict[df]["close"].ewm(span=a, min_periods=a).mean()
        df_dict[df]["ma_slow"] = df_dict[df]["close"].ewm(span=b, min_periods=b).mean()
        df_dict[df]["macd"] = df_dict[df]["ma_fast"] - df_dict[df]["ma_slow"]
        df_dict[df]["signal"] = df_dict[df]["macd"].ewm(span=c, min_periods=c).mean()
        df_dict[df].drop(["ma_fast","ma_slow"], axis=1, inplace=True)

def stochastic(df_dict, lookback=14, k=3, d=3):
    """function to calculate Stochastic Oscillator
       lookback = lookback period
       k and d = moving average window for %K and %D"""
    for df in df_dict:
        df_dict[df]["HH"] = df_dict[df]["high"].rolling(lookback).max()
        df_dict[df]["LL"] = df_dict[df]["low"].rolling(lookback).min()
        df_dict[df]["%K"] = (100 * (df_dict[df]["close"] - df_dict[df]["LL"])/(df_dict[df]["HH"]-df_dict[df]["LL"])).rolling(k).mean()
        df_dict[df]["%D"] = df_dict[df]["%K"].rolling(d).mean()
        df_dict[df].drop(["HH","LL"], axis=1, inplace=True)

def main():
    global stoch_signal
    historicalData = hist_data(tickers, start_date =time.strftime("%Y-%m-%d"), timeframe="Minute")
    MACD(historicalData)
    stochastic(historicalData)
    positions = api.list_positions()
    
    for ticker in tickers:
        historicalData[ticker].dropna(inplace=True)
        existing_pos = False
        
        if historicalData[ticker]["%K"][-1] < 20:
            stoch_signal[ticker] = "oversold"
        elif historicalData[ticker]["%K"][-1] > 80:
            stoch_signal[ticker] = "overbought"
        
        for position in positions:
            if len(positions) > 0:
                if position.symbol == ticker and position.qty !=0:
                    print("existing position of {} stocks in {}...skipping".format(position.qty, ticker))
                    existing_pos = True
        
        if historicalData[ticker]["macd"].iloc[-1]> historicalData[ticker]["signal"].iloc[-1] and \
            historicalData[ticker]["macd"].iloc[-2]< historicalData[ticker]["signal"].iloc[-2] and \
            stoch_signal[ticker]=="oversold" and existing_pos == False:
                api.submit_order(ticker, max(1,int(max_pos/historicalData[ticker]["close"].iloc[-1])), "buy", "market", "ioc")
                print("bought {} stocks in {}".format(int(max_pos/historicalData[ticker]["close"].iloc[-1]),ticker))
                time.sleep(2)
                try:
                    filled_qty = api.get_position(ticker).qty
                    time.sleep(1)
                    api.submit_order(ticker, int(filled_qty), "sell", "trailing_stop", "day", trail_percent = "1.5")
                except Exception as e:
                    print(ticker, e)


starttime = time.time()
timeout = starttime + 60*60*1
while time.time() <= timeout:
    print("starting iteration at {}".format(time.strftime("%Y-%m-%d %H:%M:%S")))
    main()
    time.sleep(60 - ((time.time() - starttime) % 60)) 

#close out all positions and orders    
api.close_all_positions()
time.sleep(5)
api.cancel_all_orders()
time.sleep(5)
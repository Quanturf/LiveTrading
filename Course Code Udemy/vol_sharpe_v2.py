# -*- coding: utf-8 -*-
"""
Alpaca API - Volatility & Sharpe implementation (V2 API)

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

import os
import json
from alpaca_trade_api.rest import REST, TimeFrame
import numpy as np

os.chdir("D:\\OneDrive\\Alpaca") #change this based on the path on your local machine

endpoint = "https://data.alpaca.markets/v2"
headers = json.loads(open("key.txt",'r').read())

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
        
data_dump = hist_data(["FB","CSCO","AMZN"], start_date ="2021-12-15", timeframe="Hour") 

#adding return column to each bar dataframe - assuming long and hold strategy
for df in data_dump:
    data_dump[df]["return"] = data_dump[df]["close"].pct_change()

def CAGR(df_dict):
    "function to calculate the Cumulative Annual Growth Rate; DF should have ret column"
    cagr = {}
    for df in df_dict:
        abs_return = (1 + df_dict[df]["return"]).cumprod().iloc[-1]
        n = len(df_dict[df])/252
        cagr[df] = (abs_return)**(1/n) - 1
    return cagr

def volatility(df_dict):
    "function to calculate annualized volatility; DF should have ret column"
    vol = {}
    for df in df_dict:
        vol[df] = df_dict[df]["return"].std() * np.sqrt(252)
    return vol

def sharpe(df_dict, rf_rate):
    "function to calculate sharpe ratio ; rf is the risk free rate"
    sharpe = {}
    cagr = CAGR(df_dict)
    vol = volatility(df_dict)
    for df in df_dict:
        sharpe[df] = (cagr[df] - rf_rate)/vol[df]
    return sharpe

sharpe(data_dump, 0.03)

      
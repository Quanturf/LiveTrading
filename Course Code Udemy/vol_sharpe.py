# -*- coding: utf-8 -*-
"""
Alpaca API - Volatility & Sharpe implementation

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

import requests
import os
import json
import pandas as pd
import numpy as np

os.chdir("D:\\Alpaca") #change this based on the path on your local machine

endpoint = "https://data.alpaca.markets/v1"
headers = json.loads(open("key.txt",'r').read())

def hist_data(symbols, timeframe="15Min", limit=200, start="", end="", after="", until=""):
    """
    returns historical bar data for a string of symbols separated by comma
    symbols should be in a string format separated by comma e.g. symbols = "MSFT,AMZN,GOOG"
    """
    df_data = {}
    bar_url = endpoint + "/bars/{}".format(timeframe)
    params = {"symbols" : symbols,
              "limit" : limit,
              "start" : start,
              "end" : end,
              "after" : after,
              "until" : until}
    r = requests.get(bar_url, headers = headers, params = params)
    json_dump = r.json()
    for symbol in json_dump:
        temp = pd.DataFrame(json_dump[symbol])
        temp.rename({"t":"time","o":"open","h":"high","l":"low","c":"close","v":"volume"},axis=1, inplace=True)
        temp["time"] = pd.to_datetime(temp["time"], unit="s")
        temp.set_index("time",inplace=True)
        temp.index = temp.index.tz_localize("UTC").tz_convert("America/Indiana/Petersburg")
        df_data[symbol] = temp
    return df_data

data_dump = hist_data("FB,MSFT,CSCO", timeframe="1D", limit=750)

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

      
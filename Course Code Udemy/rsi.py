# -*- coding: utf-8 -*-
"""
Alpaca API - Calculate and store Relative Strength Index using historical data

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
        
data_dump = hist_data("FB,CSCO,AMZN", timeframe="5Min") 


def RSI(df_dict, n=14):
    "function to calculate RSI"
    for df in df_dict:
        df_dict[df]["change"] = df_dict[df]["close"] - df_dict[df]["close"].shift(1)
        df_dict[df]["gain"] = np.where(df_dict[df]["change"]>=0, df_dict[df]["change"], 0)
        df_dict[df]["loss"] = np.where(df_dict[df]["change"]<0, -1*df_dict[df]["change"], 0)
        df_dict[df]["avgGain"] = df_dict[df]["gain"].ewm(alpha=1/n, min_periods=n).mean()
        df_dict[df]["avgLoss"] = df_dict[df]["loss"].ewm(alpha=1/n, min_periods=n).mean()
        df_dict[df]["rs"] = df_dict[df]["avgGain"]/df_dict[df]["avgLoss"]
        df_dict[df]["rsi"] = 100 - (100/ (1 + df_dict[df]["rs"]))
        df_dict[df].drop(["change","gain","loss","avgGain","avgLoss","rs"], axis=1, inplace=True)

RSI(data_dump)

        
      
# -*- coding: utf-8 -*-
"""
Alpaca API - Historical Data function and Resampling for V2 API

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

import requests
import os
import json
import pandas as pd

os.chdir("D:\\Alpaca") #change this based on the path on your local machine

endpoint = "https://data.alpaca.markets/v2"
headers = json.loads(open("key.txt",'r').read())
symbols = ["FB","CSCO","AMZN"]

def hist_data(symbols, start="2021-01-01", timeframe="1Hour", limit=600, end=""):
    """
    returns historical bar data for a string of symbols separated by comma
    symbols should be in a string format separated by comma e.g. symbols = "MSFT,AMZN,GOOG"
    """
    df_data_tickers = {}
    
    for symbol in symbols:   
        bar_url = endpoint + "/stocks/{}/bars".format(symbol)
        params = {"start":start, "limit" :limit, "timeframe":timeframe}
        
        data = {"bars": [], "next_page_token":'', "symbol":symbol}
        while True:
                r = requests.get(bar_url, headers = headers, params = params)
                r = r.json()
                if r["next_page_token"] == None:
                    data["bars"]+=r["bars"]
                    break
                else:
                    params["page_token"] = r["next_page_token"]
                    data["bars"]+=r["bars"]
                    data["next_page_token"] = r["next_page_token"]
        
        df_data = pd.DataFrame(data["bars"])
        df_data.rename({"t":"time","o":"open","h":"high","l":"low","c":"close","v":"volume"},axis=1, inplace=True)
        df_data["time"] = pd.to_datetime(df_data["time"])
        df_data.set_index("time",inplace=True)
        df_data.index = df_data.index.tz_convert("America/Indiana/Petersburg")
        
        df_data_tickers[symbol] = df_data
    return df_data_tickers
        
data_dump = hist_data(symbols, start="2021-05-15", timeframe="1Min")  


#################resampling############################
data_5m = {}
for ticker in data_dump:
    logic = {'open'  : 'first',
             'high'  : 'max',
             'low'   : 'min',
             'close' : 'last',
             'volume': 'sum'}
    data_5m[ticker] = data_dump[ticker].resample('5Min').apply(logic)
    data_5m[ticker].dropna(inplace=True)
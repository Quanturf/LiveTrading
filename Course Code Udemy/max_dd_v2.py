# -*- coding: utf-8 -*-
"""
Alpaca API - Maximum Drawdown implementation (V2 API)

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

import os
import json
from alpaca_trade_api.rest import REST, TimeFrame

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
    

def max_dd(df_dict):
    "function to calculate max drawdown"
    max_drawdown = {}
    for df in df_dict:
        df_dict[df]["cum_return"] = (1 + df_dict[df]["return"]).cumprod()
        df_dict[df]["cum_max"] = df_dict[df]["cum_return"].cummax()
        df_dict[df]["drawdown"] = df_dict[df]["cum_max"] - df_dict[df]["cum_return"]
        df_dict[df]["drawdown_pct"] = df_dict[df]["drawdown"]/df_dict[df]["cum_max"]
        max_drawdown[df] = df_dict[df]["drawdown_pct"].max()
        df_dict[df].drop(["cum_return","cum_max","drawdown","drawdown_pct"], axis=1, inplace=True)
    return max_drawdown
    
max_dd(data_dump)    
   
      
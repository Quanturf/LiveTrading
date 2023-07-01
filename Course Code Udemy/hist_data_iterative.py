# -*- coding: utf-8 -*-
"""
Alpaca API - Extracting historical data iteratively

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

import requests
import os
import json
import pandas as pd
import time

os.chdir("D:\\Alpaca") #change this based on the path on your local machine

endpoint = "https://data.alpaca.markets/v1"
headers = json.loads(open("key.txt",'r').read())

def hist_data(symbol, timeframe="15Min", limit=200, start="", end="", after="", until=""):
    """
    returns historical bar data for a string of symbols separated by comma
    symbols should be in a string format separated by comma e.g. symbols = "MSFT,AMZN,GOOG"
    """
    bar_url = endpoint + "/bars/{}".format(timeframe)
    params = {"symbols" : symbol,
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
    return temp

tickers = ["FB", "AMZN", "GOOG"]
starttime = time.time()
timeout = starttime + 60*5
while time.time() <= timeout:
    print("*****************************************************************")
    for ticker in tickers:
        print("printing data for {} at {}".format(ticker,time.time()))
        print(hist_data(ticker, timeframe="1Min"))
    time.sleep(60 - ((time.time() - starttime) % 60))
             
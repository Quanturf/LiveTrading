# -*- coding: utf-8 -*-
"""
Alpaca API - Last trade data for V2 API

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""


import requests
import os
import json

os.chdir("D:\\OneDrive\\Alpaca") #change this based on the path on your local machine

endpoint = "https://data.alpaca.markets/v2"
headers = json.loads(open("key.txt",'r').read())

def last_trade(symbol):
    "Extract last traded price and volume for one symbol"
    last_trade_url = endpoint + "/stocks/{}/trades/latest".format(symbol)
    r = requests.get(last_trade_url, headers = headers)
    return (r.json()["trade"]["p"], r.json()["trade"]["s"])

def last_trade_multi(symbols):
    "Extract last traded price and volume for multiple symbols"
    ltp_vol = {}
    last_trade_url = endpoint + "/stocks/trades/latest"
    params = {"symbols":symbols}
    r = requests.get(last_trade_url, headers = headers, params = params)
    for symbol in symbols.split(","):
        ltp_vol[symbol] = [r.json()["trades"][symbol]["p"], r.json()["trades"][symbol]["s"]]
    return ltp_vol


price,volume = last_trade("CSCO")
ltp_vol = last_trade_multi("CSCO,AAPL,INTC")
# -*- coding: utf-8 -*-
"""
Alpaca API - Orders API (Market & Limit)

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

import requests
import os
import json

os.chdir("D:\\Alpaca") #change this based on the path on your local machine

endpoint = "https://paper-api.alpaca.markets"
headers = json.loads(open("key.txt",'r').read())

def market_order(symbol, quantity, side="buy", tif="day"):
    ord_url = endpoint + "/v2/orders"
    params = {"symbol": symbol,
              "qty": quantity,
              "side" : side,
              "type": "market",
              "time_in_force": tif}
    r = requests.post(ord_url, headers=headers, json=params)
    return r.json()

market_order("AMZN", 1) 

def limit_order(symbol, quantity, limit_pr, side="buy", tif="day"):
    ord_url = endpoint + "/v2/orders"
    params = {"symbol": symbol,
              "qty": quantity,
              "side" : side,
              "type": "limit",
              "limit_price" : limit_pr,
              "time_in_force": tif}
    r = requests.post(ord_url, headers=headers, json=params)
    return r.json()
  
limit_order("AMZN", 1, limit_pr = 3202)


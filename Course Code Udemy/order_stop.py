# -*- coding: utf-8 -*-
"""
Alpaca API - Orders API (Stop & Stop Limit)

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

import requests
import os
import json

os.chdir("D:\\Alpaca") #change this based on the path on your local machine

endpoint = "https://paper-api.alpaca.markets"
headers = json.loads(open("key.txt",'r').read())

def stop_order(symbol, quantity, stop_pr, side="buy", tif="day"):
    ord_url = endpoint + "/v2/orders"
    params = {"symbol": symbol,
              "qty": quantity,
              "side" : side,
              "type": "stop",
              "stop_price": stop_pr,
              "time_in_force": tif}
    r = requests.post(ord_url, headers=headers, json=params)
    return r.json()

stop_order("AMZN", 1, 3185, "sell")

def stop_limit_order(symbol, quantity, stop_pr, limit_pr, side="buy", tif="day"):
    ord_url = endpoint + "/v2/orders"
    params = {"symbol": symbol,
              "qty": quantity,
              "side" : side,
              "type": "stop_limit",
              "stop_price": stop_pr,
              "limit_price" : limit_pr,
              "time_in_force": tif}
    r = requests.post(ord_url, headers=headers, json=params)
    return r.json()

stop_limit_order("AMZN", 1, 3175, 3175, "sell")



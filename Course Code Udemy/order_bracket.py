"""
Alpaca API - Orders API (Bracket Order)

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

import requests
import os
import json

os.chdir("D:\\Alpaca") #change this based on the path on your local machine

endpoint = "https://paper-api.alpaca.markets"
headers = json.loads(open("key.txt",'r').read())

def bracket_order(symbol, quantity, tplp, slsp, sllp, side="buy", tif="day"):
    ord_url = endpoint + "/v2/orders"
    params = {
              "symbol": symbol,
              "qty": quantity,
              "side" : side,
              "type": "market",
              "time_in_force": tif,
              "order_class": "bracket",
              "take_profit" : {
                              "limit_price":tplp
                              },
              "stop_loss" : {
                            "stop_price": slsp,
                            "limit_price": sllp
                            }
              }
    r = requests.post(ord_url, headers=headers, json=params)
    return r.json()

bracket_order("AAPL", 1, 139, 126, 126)
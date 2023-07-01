# -*- coding: utf-8 -*-
"""
Alpaca API - Alpaca Python Client placing orders

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""


import alpaca_trade_api as tradeapi
import os
import json

os.chdir("D:\\Alpaca")
key = json.loads(open("key.txt","r").read())

#creating the API object
api = tradeapi.REST(key["APCA-API-KEY-ID"], key["APCA-API-SECRET-KEY"], base_url='https://paper-api.alpaca.markets')

api.submit_order("GOOG", 1, "sell", "market", "day")
api.submit_order("CSCO", 10, "buy", "limit", "day", "44.8")
api.submit_order("FB", 10, "sell", "stop", "day", stop_price = "271")
api.submit_order("CSCO", 10, "sell", "trailing_stop", "day", trail_price = "3")
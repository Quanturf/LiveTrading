# -*- coding: utf-8 -*-
"""
Alpaca API - Last trade data

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""


import requests
import os
import json

os.chdir("D:\\Alpaca") #change this based on the path on your local machine

endpoint = "https://data.alpaca.markets/v1"
headers = json.loads(open("key.txt",'r').read())

def last_trade(symbol):
    last_trade_url = endpoint + "/last/stocks/{}".format(symbol)
    r = requests.get(last_trade_url, headers = headers)
    return (r.json()["last"]["price"], r.json()["last"]["size"])

price,volume = last_trade("CSCO")
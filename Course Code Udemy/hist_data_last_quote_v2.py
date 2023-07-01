# -*- coding: utf-8 -*-
"""
Alpaca API - Last trade data

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""


import requests
import os
import json

os.chdir("D:\\OneDrive\\Alpaca") #change this based on the path on your local machine

endpoint = "https://data.alpaca.markets/v2"
headers = json.loads(open("key.txt",'r').read())

def last_quote(symbol):
    "Extract last traded price and volume for one symbol"
    last_quote_url = endpoint + "/stocks/{}/quotes".format(symbol)
    r = requests.get(last_quote_url, headers = headers)
    bid_price = r.json()["quotes"][0]["bp"]
    ask_price = r.json()["quotes"][0]["ap"]
    bid_vol = r.json()["quotes"][0]["bs"]
    ask_vol = r.json()["quotes"][0]["as"]
    return [bid_price,ask_price,bid_vol,ask_vol]

last_quote("CSCO")
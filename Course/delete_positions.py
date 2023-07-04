import requests
import os
import json

os.chdir("D:\Course")

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

def del_positions(symbol="", qty=0):
    if len(symbol)>1:
        pos_url = endpoint + "/v2/positions/{}".format(symbol)
        params = {"qty" : qty}
    else:
        pos_url = endpoint + "/v2/positions"
        params = {}
    r = requests.delete(pos_url, headers=headers, json=params)
    return r.json()

market_order("CSCO", 10, "sell") #initiate a short position in CSCO
market_order("GOOG", 2, "buy") #initiate a long position in GOOG
market_order("INTC", 5, "buy") ##initiate a long position in INTC
del_positions("CSCO") #delete CSCO position
del_positions() #delete all positions
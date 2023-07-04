import requests
import os
import json
os.chdir("D:\Course")
endpoint = "https://data.alpaca.markets/v1"
headers = json.loads(open("key.txt",'r').read())

def last_trade(symbol):
    last_trade_url = endpoint + "/last/stocks/{}".format(symbol)
    r = requests.get(last_trade_url, headers = headers)
    return (r.json()["last"]["price"], r.json()["last"]["size"])

price,volume = last_trade("CSCO")
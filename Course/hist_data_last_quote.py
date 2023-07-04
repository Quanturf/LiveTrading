import requests
import os
import json

os.chdir("D:\Course")

endpoint = "https://data.alpaca.markets/v1"
headers = json.loads(open("key.txt",'r').read())

def last_quote(symbol):
    last_quote_url = endpoint + "/last_quote/stocks/{}".format(symbol)
    r = requests.get(last_quote_url, headers = headers)
    return r.json()

last_quote("CSCO")
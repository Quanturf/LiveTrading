
import requests
import os
import json

os.chdir("D:\Course")

endpoint = "https://data.alpaca.markets/v1"
headers = json.loads(open("key.txt",'r').read())

timeframe = "15Min"
bar_url = endpoint + "/bars/{}".format(timeframe)
params = {"symbols" : "MSFT,AAPL",
          "limit" : 200}

r = requests.get(bar_url, headers = headers, params = params)

data = r.json()

print(data)

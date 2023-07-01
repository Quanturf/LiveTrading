# -*- coding: utf-8 -*-
"""
Alpaca API - Historical Data

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

import requests
import os
import json

os.chdir("D:\\Alpaca") #change this based on the path on your local machine

endpoint = "https://data.alpaca.markets/v1"
headers = json.loads(open("key.txt",'r').read())

timeframe = "15Min"
bar_url = endpoint + "/bars/{}".format(timeframe)
params = {"symbols" : "MSFT,AAPL",
          "limit" : 200}

r = requests.get(bar_url, headers = headers, params = params)

data = r.json()


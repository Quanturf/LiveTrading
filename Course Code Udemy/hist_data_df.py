# -*- coding: utf-8 -*-
"""
Alpaca API - Historical Data dataframe

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

import requests
import os
import json
import pandas as pd

os.chdir("D:\\Alpaca") #change this based on the path on your local machine

endpoint = "https://data.alpaca.markets/v1"
headers = json.loads(open("key.txt",'r').read())

timeframe = "15Min"
bar_url = endpoint + "/bars/{}".format(timeframe)
params = {"symbols" : "MSFT,AAPL",
          "limit" : 200}

r = requests.get(bar_url, headers = headers, params = params)

data = r.json()


temp = data["MSFT"]
temp = pd.DataFrame(temp)
temp.rename({"t":"time","o":"open","h":"high","l":"low","c":"close","v":"volume"},axis=1, inplace=True)
temp["time"] = pd.to_datetime(temp["time"], unit="s")
temp.set_index("time",inplace=True)
temp.index = temp.index.tz_localize("UTC").tz_convert("America/Indiana/Petersburg")
print("hello word")

import requests
import os
import json

os.chdir("D:\Course")

url= "https://data.alpaca.markets/v1"

headers=json.loads(open("key.txt",'r').read())

timeframe="30Min"

bar_url=url+"/bars/{}".format(timeframe)

print(bar_url)

params={
          "symbols":"MSFT,AAPL",
          "limit":200
        }

r=requests.get(bar_url,headers=headers,params=params)

print(r.text)
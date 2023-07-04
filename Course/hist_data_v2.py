import requests
import os
import json
import pandas as pd

os.chdir("D:\Course")

endpoint = "https://data.alpaca.markets/v2"
headers = json.loads(open("key.txt",'r').read())

symbol = "MSFT"
bar_url = endpoint + "/stocks/{}/bars".format(symbol)
params = {"start":"2020-05-15","limit" : 900, "timeframe":"1Hour"}

data = {"bars": [], "next_page_token":'', "symbol":symbol}
while True:
    r = requests.get(bar_url, headers = headers, params = params)
    r = r.json()
    if r["next_page_token"] == None:
        data["bars"]+=r["bars"]
        break
    else:
        params["page_token"] = r["next_page_token"]
        data["bars"]+=r["bars"]
        data["next_page_token"] = r["next_page_token"]
        


df_data = pd.DataFrame(data["bars"])
df_data.rename({"t":"time","o":"open","h":"high","l":"low","c":"close","v":"volume"},axis=1, inplace=True)
df_data["time"] = pd.to_datetime(df_data["time"])
df_data.set_index("time",inplace=True)
df_data.index = df_data.index.tz_convert("America/Indiana/Petersburg")
import requests
import os
import json
import pandas as pd

os.chdir("D:\Course")

endpoint = "https://data.alpaca.markets/v1"
headers = json.loads(open("key.txt",'r').read())

def hist_data(symbols, timeframe="15Min", limit=200, start="", end="", after="", until=""):
    """
    returns historical bar data for a string of symbols separated by comma
    symbols should be in a string format separated by comma e.g. symbols = "MSFT,AMZN,GOOG"
    """
    df_data = {}
    bar_url = endpoint + "/bars/{}".format(timeframe)
    params = {"symbols" : symbols,
              "limit" : limit,
              "start" : start,
              "end" : end,
              "after" : after,
              "until" : until}
    r = requests.get(bar_url, headers = headers, params = params)
    json_dump = r.json()
    for symbol in json_dump:
        temp = pd.DataFrame(json_dump[symbol])
        temp.rename({"t":"time","o":"open","h":"high","l":"low","c":"close","v":"volume"},axis=1, inplace=True)
        temp["time"] = pd.to_datetime(temp["time"], unit="s")
        temp.set_index("time",inplace=True)
        temp.index = temp.index.tz_localize("UTC").tz_convert("America/Indiana/Petersburg")
        df_data[symbol] = temp
    return df_data
        
data_dump = hist_data("FB,CSCO,AMZN", timeframe="5Min") 

def bollBand(df_dict, n=20):
    "function to calculate Bollinger Band"
    for df in df_dict:
        df_dict[df]["MB"] = df_dict[df]["close"].rolling(n).mean()
        df_dict[df]["UB"] = df_dict[df]["MB"] + 2*df_dict[df]["close"].rolling(n).std(ddof=0) #ddof=0 is required since we want to take the standard deviation of the population and not sample
        df_dict[df]["LB"] = df_dict[df]["MB"] - 2*df_dict[df]["close"].rolling(n).std(ddof=0) #ddof=0 is required since we want to take the standard deviation of the population and not sample
        df_dict[df]["BB_Width"] = df_dict[df]["UB"] -  df_dict[df]["LB"] 
        
print(bollBand(data_dump))
      

import requests
import os
import json
import pandas as pd

os.chdir("D:\Course")

endpoint = "https://data.alpaca.markets/v2"
headers = json.loads(open("key.txt",'r').read())
symbols = "INTC,CSCO,AMZN"

def hist_data_multibars(symbols, start="2022-10-01", timeframe="1Hour", limit=600, end=""):
    """
    returns historical bar data for a string of symbols separated by comma
    symbols should be in a string format separated by comma e.g. symbols = "MSFT,AMZN,GOOG"
    """
    df_data_tickers = {} 
    bar_url = endpoint + "/stocks/bars"
    params = {"symbols": symbols, "start":start, "limit" :limit, "timeframe":timeframe}
    
    data = {"bars": {}}
    while True:
        r = requests.get(bar_url, headers = headers, params = params)
        r = r.json()
        print(r["next_page_token"])            
        for symbol in r["bars"]:
            if symbol not in data["bars"]:
                data["bars"][symbol] = r["bars"][symbol]
            else:
                data["bars"][symbol] +=r["bars"][symbol]
        if r["next_page_token"] == None:
            break
        else:
            params["page_token"] = r["next_page_token"]
            
    
    for symbol in data["bars"]:
        df_data = pd.DataFrame(data["bars"][symbol])
        df_data.rename({"t":"time","o":"open","h":"high","l":"low","c":"close","v":"volume"},axis=1, inplace=True)
        df_data["time"] = pd.to_datetime(df_data["time"])
        df_data.set_index("time",inplace=True)
        df_data.index = df_data.index.tz_convert("America/Indiana/Petersburg")
    
        df_data_tickers[symbol] = df_data
    return df_data_tickers
        
data_dump = hist_data_multibars(symbols, start="2022-10-24", timeframe="1Min")  


#################resampling############################
data_5m = {}
for ticker in data_dump:
    logic = {'open'  : 'first',
             'high'  : 'max',
             'low'   : 'min',
             'close' : 'last',
             'volume': 'sum'}
    data_5m[ticker] = data_dump[ticker].resample('5Min').apply(logic)
    data_5m[ticker].dropna(inplace=True)
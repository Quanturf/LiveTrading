# -*- coding: utf-8 -*-
"""
Alpaca API - Finding top movers using streaming

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""


import websocket
import os
import json
import requests
import threading
import pandas as pd
import time

os.chdir("D:\\Alpaca") #change this based on the path on your local machine

endpoint = "https://data.alpaca.markets/v1"
headers = json.loads(open("key.txt",'r').read())
tickers = "FB,AMZN,INTC,MSFT,AAPL,GOOG,CSCO,CMCSA,ADBE,NVDA,NFLX,PYPL,AMGN,AVGO,TXN,CHTR,QCOM,GILD,FISV,BKNG,INTU,ADP,CME,TMUS,MU"
streams = ["T.{}".format(i) for i in tickers.split(",")]
ltp = {}
prev_close = {}
perc_change = {}

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

    
data_dump = hist_data(tickers, timeframe="1D")
for ticker in tickers.split(","):
    prev_close[ticker] = data_dump[ticker]["close"][-2]
    ltp[ticker] = data_dump[ticker]["close"][-1]
    perc_change[ticker] = 0

def on_open(ws):
    auth = {
            "action": "authenticate",
            "data": {"key_id": headers["APCA-API-KEY-ID"],"secret_key": headers["APCA-API-SECRET-KEY"]}
           }
    
    ws.send(json.dumps(auth))
    
    message = {
                "action": "listen",
                "data": {
                         "streams": streams
                        }
              }
                
    ws.send(json.dumps(message))
 
def on_message(ws, message):
    #print(message)
    tick = json.loads(message)
    tkr = tick["stream"].split(".")[-1]
    ltp[tkr] = float(tick["data"]["p"])
    perc_change[tkr] = round((ltp[tkr]/prev_close[tkr] - 1)*100,2)   
    

def connect():
    ws = websocket.WebSocketApp("wss://data.alpaca.markets/stream", on_open=on_open, on_message=on_message)
    ws.run_forever()


con_thread = threading.Thread(target=connect)
con_thread.start()

starttime = time.time()
timeout = starttime + 60*5
while time.time() <= timeout:
    for ticker in tickers.split(","):
        print("percent change for {} = {}".format(ticker,perc_change[ticker]))
    time.sleep(60 - ((time.time() - starttime) % 60))
    


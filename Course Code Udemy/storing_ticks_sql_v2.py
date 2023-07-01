"""
Alpaca API - Storing streaming ticks in sql database V2 api

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

import websocket
import os
import json
import sqlite3
import datetime as dt
import dateutil.parser

os.chdir("D:\\OneDrive\\Alpaca") #change this based on the path on your local machine

endpoint = "wss://stream.data.alpaca.markets/v2/iex"
headers = json.loads(open("key.txt",'r').read())
tickers = ["AAPL", "TSLA", "GOOG", "AMZN"]

db = sqlite3.connect('D:/OneDrive/Alpaca/4_streaming/ticks_v2.db')

def create_tables(tickers):
    c = db.cursor()
    for ticker in tickers:
        c.execute("CREATE TABLE IF NOT EXISTS {} (timestamp datetime primary key, price real(15,5), volume integer)".format(ticker))
    try:
        db.commit()
    except:
        db.rollback()
        
create_tables(tickers)


def on_open(ws):
    auth = {"action": "auth", "key": headers["APCA-API-KEY-ID"], "secret": headers["APCA-API-SECRET-KEY"]}
   
    ws.send(json.dumps(auth))
    
    message = {"action":"subscribe","trades":tickers}
                
    ws.send(json.dumps(message))

def on_message(ws, message):
    print(message)
    tick = json.loads(message)
    print(dateutil.parser.isoparse(tick[0]["t"]))
    c = db.cursor()
    for ms in range(100):
        try:        
            tabl = tick[0]["S"]
            vals = [dateutil.parser.isoparse(tick[0]["t"])+dt.timedelta(microseconds=ms),tick[0]["p"],tick[0]["s"]]
            query = "INSERT INTO {}(timestamp,price,volume) VALUES (?,?,?)".format(tabl)
            c.execute(query,vals)
            break
        except Exception as e:
            print(e)
        
    try:
        db.commit()
    except:
        db.rollback()   

ws = websocket.WebSocketApp(endpoint, on_open=on_open, on_message=on_message)
ws.run_forever()
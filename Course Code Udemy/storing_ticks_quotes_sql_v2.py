"""
Alpaca API - Storing streaming ticks in sql database using V2 API

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
trade_tickers = ["AAPL", "TSLA", "GOOG", "AMZN"]
quote_tickers = ["AAPL", "TSLA", "GOOG", "AMZN"]

db1 = sqlite3.connect('D:/OneDrive/Alpaca/4_streaming/trades_ticks_v2.db')
db2 = sqlite3.connect('D:/OneDrive/Alpaca/4_streaming/quotes_ticks_v2.db')


def create_tables(db, tickers, tick_type):
    c = db.cursor()
    if tick_type == "trades":
        for ticker in tickers:
            c.execute("CREATE TABLE IF NOT EXISTS {} (timestamp datetime primary key, price real(15,5), volume integer)".format(ticker))
    if tick_type == "quotes":
        for ticker in tickers:
            c.execute("CREATE TABLE IF NOT EXISTS {} (timestamp datetime primary key, bid_price real(15,5), ask_price real(15,5), bid_volume integer, ask_volume integer)".format(ticker))
    try:
        db.commit()
    except:
        db.rollback()
        
create_tables(db1,trade_tickers,"trades")
create_tables(db2,quote_tickers,"quotes")

def insert_ticks(tick):
    if tick[0]["T"] == "q":
        c = db2.cursor()
        for ms in range(100):
            try:        
                tabl = tick[0]["S"]
                vals = [dateutil.parser.isoparse(tick[0]["t"])+dt.timedelta(microseconds=ms),tick[0]["bp"],tick[0]["ap"],tick[0]["bs"],tick[0]["as"]]
                query = "INSERT INTO {}(timestamp,bid_price,ask_price,bid_volume,ask_volume) VALUES (?,?,?,?,?)".format(tabl)
                c.execute(query,vals)
                break
            except Exception as e:
                print(e)
        try:
            db2.commit()
        except:
            db2.rollback()
            
    if tick[0]["T"] == "t":
        c = db1.cursor()
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
            db1.commit()
        except:
            db1.rollback()

def on_open(ws):
    auth = {"action": "auth", "key": headers["APCA-API-KEY-ID"], "secret": headers["APCA-API-SECRET-KEY"]}
    
    ws.send(json.dumps(auth))
    
    message = {"action":"subscribe","trades":trade_tickers,"quotes":quote_tickers}
                
    ws.send(json.dumps(message))

def on_message(ws, message):
    print(message)
    tick = json.loads(message)
    insert_ticks(tick)  

ws = websocket.WebSocketApp(endpoint, on_open=on_open, on_message=on_message)
ws.run_forever()
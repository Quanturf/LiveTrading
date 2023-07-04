import websocket
import os
import json
import sqlite3
import datetime as dt

os.chdir("D:\Course")

endpoint = "wss://data.alpaca.markets/stream"
headers = json.loads(open("key.txt",'r').read())
streams = ["T.AAPL", "T.TSLA", "T.GOOG", "T.AMZN"]

db = sqlite3.connect('D:/Alpaca/4_streaming/ticks.db')

def create_tables(tickers):
    c = db.cursor()
    for ticker in tickers:
        c.execute("CREATE TABLE IF NOT EXISTS {} (timestamp datetime primary key, price real(15,5), volume integer)".format(ticker))
    try:
        db.commit()
    except:
        db.rollback()
        
create_tables([i.split(".")[-1] for i in streams])


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
    print(message)
    tick = json.loads(message)
    c = db.cursor()
    for ms in range(100):
        try:        
            tabl = tick["stream"].split(".")[-1]
            vals = [dt.datetime.fromtimestamp(int(tick["data"]["t"])/10**9)+dt.timedelta(milliseconds=ms),tick["data"]["p"],tick["data"]["s"]]
            query = "INSERT INTO {}(timestamp,price,volume) VALUES (?,?,?)".format(tabl)
            c.execute(query,vals)
            break
        except Exception as e:
            print(e)
    try:
        db.commit()
    except:
        db.rollback()   

ws = websocket.WebSocketApp("wss://data.alpaca.markets/stream", on_open=on_open, on_message=on_message)
ws.run_forever()
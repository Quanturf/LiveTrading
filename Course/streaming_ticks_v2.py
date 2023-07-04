import websocket
import os
import json

os.chdir("D:\Course")

endpoint = "wss://stream.data.alpaca.markets/v2/iex"
headers = json.loads(open("key.txt",'r').read())

def on_open(ws):
    auth = {"action": "auth", "key": headers["APCA-API-KEY-ID"], "secret": headers["APCA-API-SECRET-KEY"]}
    
    ws.send(json.dumps(auth))
    
    message = {"action":"subscribe","trades":["AAPL"],"quotes":["AMD","CSCO"],"bars":["FB","INTC"]}
                
    ws.send(json.dumps(message))
 
def on_message(ws, message):
    print(message)

ws = websocket.WebSocketApp(endpoint, on_open=on_open, on_message=on_message)
ws.run_forever()
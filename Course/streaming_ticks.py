import websocket
import os
import json

os.chdir("D:\Course")

endpoint = "wss://data.alpaca.markets/stream"
headers = json.loads(open("key.txt",'r').read())
streams = ["T.AAPL", "T.TSLA", "Q.GOOG", "AM.FB"]

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

ws = websocket.WebSocketApp("wss://data.alpaca.markets/stream", on_open=on_open, on_message=on_message)
ws.run_forever()
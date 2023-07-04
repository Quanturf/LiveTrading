import websocket
import os
import json
import threading
import time
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST, TimeFrame

os.chdir("D:\Course")

endpoint = "https://data.alpaca.markets/v2"
headers = json.loads(open("key.txt",'r').read())
api = tradeapi.REST(headers["APCA-API-KEY-ID"], headers["APCA-API-SECRET-KEY"], base_url='https://paper-api.alpaca.markets')
tickers = ['FB','AMZN','INTC','MSFT','AAPL','GOOG','CSCO','CMCSA','ADBE',
           'NVDA','NFLX','PYPL','AMGN','AVGO','TXN','CHTR','QCOM','GILD',
           'FISV','BKNG','INTU','ADP','CME','TMUS','MU']
ltp = {} #dictionary to store ltp information for each ticker
prev_close = {} #dictionary to store previous day's close price information for each ticker 
perc_change = {} #dictionary to store percentage change from yesterday's close for each ticker
traded_tickers = [] #storing tickers which have been traded and therefore to be excluded
max_pos = 3000 #max position size for each ticker

def hist_data(symbols, start_date ="2022-02-01", timeframe="Minute"):
    """
    returns historical bar data for a list of tickers e.g. symbols = ["MSFT,AMZN,GOOG"]
    """
    df_data = {}
    api = REST(headers["APCA-API-KEY-ID"], headers["APCA-API-SECRET-KEY"], base_url=endpoint)
    for ticker in symbols:
        if timeframe == "Minute":
            df_data[ticker] = api.get_bars(ticker, TimeFrame.Minute, start_date, adjustment='all').df
        elif timeframe == "Hour":
            df_data[ticker] = api.get_bars(ticker, TimeFrame.Hour, start_date, adjustment='all').df
        else:
            df_data[ticker] = api.get_bars(ticker, TimeFrame.Day, start_date, adjustment='all').df
    return df_data

    
data_dump = hist_data(tickers, timeframe="Day")

#initializing the dictionaries
for ticker in tickers:
    prev_close[ticker] = data_dump[ticker]["close"][-2]
    ltp[ticker] = data_dump[ticker]["close"][-1]
    perc_change[ticker] = 0

def on_open(ws):
    auth = {"action": "auth", "key": headers["APCA-API-KEY-ID"], "secret": headers["APCA-API-SECRET-KEY"]}
    
    ws.send(json.dumps(auth))
    
    message = {"action":"subscribe","trades":tickers}
                
    ws.send(json.dumps(message))
 
def on_message(ws, message):
    print(message)
    tick = json.loads(message)
    tkr = tick[0]["S"]
    ltp[tkr] = float(tick[0]["p"])
    perc_change[tkr] = round((ltp[tkr]/prev_close[tkr] - 1)*100,2)   
    

def connect():
    ws = websocket.WebSocketApp("wss://stream.data.alpaca.markets/v2/iex", on_open=on_open, on_message=on_message)
    ws.run_forever()

def pos_size(ticker):
    return max(1,int(max_pos/ltp[ticker]))

def signal(traded_tickers):
    #print(traded_tickers)
    for ticker, pc in perc_change.items():
        #   (ticker, pc)
        if pc > 2 and ticker not in traded_tickers:
            api.submit_order(ticker, pos_size(ticker), "buy", "market", "ioc")
            time.sleep(2)
            try:
                filled_qty = api.get_position(ticker).qty
                time.sleep(1)
                api.submit_order(ticker, int(filled_qty), "sell", "trailing_stop", "day", trail_percent = "1.5")
                traded_tickers.append(ticker)
            except Exception as e:
                print(ticker, e)
        if pc < -2 and ticker not in traded_tickers:
            api.submit_order(ticker, pos_size(ticker), "sell", "market", "ioc")
            time.sleep(2)
            try:
                filled_qty = api.get_position(ticker).qty
                time.sleep(1)
                api.submit_order(ticker, -1*int(filled_qty), "buy", "trailing_stop", "day", trail_percent = "1.5")
                traded_tickers.append(ticker)
            except Exception as e:
                print(ticker, e)

con_thread = threading.Thread(target=connect, daemon=True)
con_thread.start()

starttime = time.time()
timeout = starttime + 60*5
while time.time() <= timeout:
    for ticker in tickers:
        print("percent change for {} = {}".format(ticker,perc_change[ticker]))
        signal(traded_tickers)
    time.sleep(60 - ((time.time() - starttime) % 60))

#closing all positions and cancelling all orders at the end of the strategy  
api.close_all_positions()
api.cancel_all_orders()
time.sleep(5)

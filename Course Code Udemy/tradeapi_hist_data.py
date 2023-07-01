"""
Alpaca API - Historical Data using alpaca python library

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

import alpaca_trade_api as tradeapi
import os
import json

os.chdir("D:\\Alpaca")
key = json.loads(open("key.txt","r").read())

#creating the API object
api = tradeapi.REST(key["APCA-API-KEY-ID"], key["APCA-API-SECRET-KEY"], base_url='https://paper-api.alpaca.markets')

#fetching historical bar data for tickers
data = api.get_barset("FB,CSCO,INTC",limit=100,timeframe="15Min")
data["FB"][-1].c #extracting close price of the latest 5 minute candle of facebook

#fetching last quote information
api.get_last_quote("CSCO")
api.get_last_quote("CSCO").askprice #getting only the required elemnt of the quote


#gfetching last trade information
api.get_last_trade("AMZN")
api.get_last_trade("AMZN").price #getting last traded price of Amazon

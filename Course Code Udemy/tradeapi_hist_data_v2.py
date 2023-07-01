# -*- coding: utf-8 -*-
"""
Alpaca API - Alpaca Python API Historical Data using V2

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""


import os
import json
from alpaca_trade_api.rest import REST, TimeFrame


os.chdir("D:\\OneDrive\\Alpaca")
key = json.loads(open("key.txt","r").read())

#creating the API object
api = REST(key["APCA-API-KEY-ID"], key["APCA-API-SECRET-KEY"], base_url='https://data.alpaca.markets/v2')

#getting historical bar deta
data = api.get_bars("AAPL", TimeFrame.Minute, "2021-12-14", "2021-12-15", adjustment='all').df

#getting historical trade deta
trades = api.get_trades("GOOG", "2021-12-14", "2021-12-15", limit=3).df

#getting historical quote deta
quotes = api.get_quotes("AMZN", limit=10).df
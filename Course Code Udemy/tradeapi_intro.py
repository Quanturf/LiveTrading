"""
Alpaca API - Alpaca Python API Library Intro

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

import alpaca_trade_api as tradeapi
import os
import json

os.chdir("D:\\Alpaca")
key = json.loads(open("key.txt","r").read())

#creating the API object
api = tradeapi.REST(key["APCA-API-KEY-ID"], key["APCA-API-SECRET-KEY"], base_url='https://paper-api.alpaca.markets')

#getting account information
account_info = api.get_account()
account_info.equity #accessing relavant information from a given position

#getting list of all positions
pos_list = api.list_positions()
pos_list[0].symbol #accessing relavant information from a given position
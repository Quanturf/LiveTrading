# -*- coding: utf-8 -*-
"""
Alpaca API - converting ticks to candles

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""


import sqlite3
import pandas as pd

db = sqlite3.connect('D:/Alpaca/4_streaming/ticks.db')

def get_bars(db, ticker, day, period):
    data = pd.read_sql("SELECT * FROM {} WHERE timestamp >= date() - '{} days'".format(ticker, day), con = db)
    data.set_index(['timestamp'], inplace=True)
    data.index = pd.to_datetime(data.index)
    price_ohlc = data.loc[:,['price']].resample(period).ohlc().dropna()
    price_ohlc.columns = ["open","high","low","close"]
    vol_ohlc = data.loc[:,['volume']].resample(period).apply({'volume':'sum'}).dropna()
    df = price_ohlc.merge(vol_ohlc, left_index=True, right_index=True)
    return df

get_bars(db,"TSLA",5, '1min')
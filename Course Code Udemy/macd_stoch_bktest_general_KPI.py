# -*- coding: utf-8 -*-
"""
Alpaca API - MACD + stochastic strategy bactesting using General KPIs

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

import requests
import os
import json
import pandas as pd
from copy import deepcopy
import numpy as np

os.chdir("D:\\Alpaca") #change this based on the path on your local machine

endpoint = "https://data.alpaca.markets/v1"
headers = json.loads(open("key.txt",'r').read())
tickers = "FB,AMZN,INTC,MSFT,AAPL,GOOG,CSCO,CMCSA,ADBE,NVDA,NFLX,PYPL,AMGN,AVGO,TXN,CHTR,QCOM,GILD,FISV,BKNG,INTU,ADP,CME,TMUS,MU"

def hist_data(symbols, timeframe="15Min", limit=200, start="", end="", after="", until=""):
    """
    returns historical bar data for a string of symbols separated by comma
    symbols should be in a string format separated by comma e.g. symbols = "MSFT,AMZN,GOOG"
    """
    df_data = {}
    bar_url = endpoint + "/bars/{}".format(timeframe)
    params = {"symbols" : symbols,
              "limit" : limit,
              "start" : start,
              "end" : end,
              "after" : after,
              "until" : until}
    r = requests.get(bar_url, headers = headers, params = params)
    json_dump = r.json()
    for symbol in json_dump:
        temp = pd.DataFrame(json_dump[symbol])
        temp.rename({"t":"time","o":"open","h":"high","l":"low","c":"close","v":"volume"},axis=1, inplace=True)
        temp["time"] = pd.to_datetime(temp["time"], unit="s")
        temp.set_index("time",inplace=True)
        temp.index = temp.index.tz_localize("UTC").tz_convert("America/Indiana/Petersburg")
        temp.between_time('09:31', '16:00')
        df_data[symbol] = temp
    return df_data

def MACD(df_dict, a=12 ,b=26, c=9):
    """function to calculate MACD
       typical values a(fast moving average) = 12; 
                      b(slow moving average) =26; 
                      c(signal line ma window) =9"""
    for df in df_dict:
        df_dict[df]["ma_fast"] = df_dict[df]["close"].ewm(span=a, min_periods=a).mean()
        df_dict[df]["ma_slow"] = df_dict[df]["close"].ewm(span=b, min_periods=b).mean()
        df_dict[df]["macd"] = df_dict[df]["ma_fast"] - df_dict[df]["ma_slow"]
        df_dict[df]["signal"] = df_dict[df]["macd"].ewm(span=c, min_periods=c).mean()
        df_dict[df].drop(["ma_fast","ma_slow"], axis=1, inplace=True)

def stochastic(df_dict, lookback=14, k=3, d=3):
    """function to calculate Stochastic Oscillator
       lookback = lookback period
       k and d = moving average window for %K and %D"""
    for df in df_dict:
        df_dict[df]["HH"] = df_dict[df]["high"].rolling(lookback).max()
        df_dict[df]["LL"] = df_dict[df]["low"].rolling(lookback).min()
        df_dict[df]["%K"] = (100 * (df_dict[df]["close"] - df_dict[df]["LL"])/(df_dict[df]["HH"]-df_dict[df]["LL"])).rolling(k).mean()
        df_dict[df]["%D"] = df_dict[df]["%K"].rolling(d).mean()
        df_dict[df].drop(["HH","LL"], axis=1, inplace=True)
 

def winRate(DF):
    "function to calculate win rate of intraday trading strategy"
    df = DF["return"]
    pos = df[df>1]
    neg = df[df<1]
    return (len(pos)/len(pos+neg))*100

def meanretpertrade(DF):
    df = DF["return"]
    df_temp = (df-1).dropna()
    return df_temp[df_temp!=0].mean()

def meanretwintrade(DF):
    df = DF["return"]
    df_temp = (df-1).dropna()
    return df_temp[df_temp>0].mean()

def meanretlostrade(DF):
    df = DF["return"]
    df_temp = (df-1).dropna()
    return df_temp[df_temp<0].mean()

def maxconsectvloss(DF):
    df = DF["return"]
    df_temp = df.dropna(axis=0)
    df_temp2 = np.where(df_temp<1,1,0)
    count_consecutive = []
    seek = 0
    for i in range(len(df_temp2)):
        if df_temp2[i] == 0:
            if seek > 0:
                count_consecutive.append(seek)
            seek = 0
        else:
            seek+=1
    if len(count_consecutive) > 0:
        return max(count_consecutive)
    else:
        return 0
    
def CAGR(DF):
    "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
    df = DF.copy()
    df["cum_return"] = (1 + df["ret"]).cumprod()
    n = len(df)/(252*26) #26 15-minute candles each trading day
    CAGR = (df["cum_return"].tolist()[-1])**(1/n) - 1
    return CAGR

def volatility(DF):
    "function to calculate annualized volatility of a trading strategy"
    df = DF.copy()
    vol = df["ret"].std() * np.sqrt(252*26)
    return vol

def sharpe(DF,rf):
    "function to calculate sharpe ratio ; rf is the risk free rate"
    df = DF.copy()
    sr = (CAGR(df) - rf)/volatility(df)
    return sr

def max_dd(DF):
    "function to calculate max drawdown"
    df = DF.copy()
    df["cum_return"] = (1 + df["ret"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    df["drawdown_pct"] = df["drawdown"]/df["cum_roll_max"]
    max_dd = df["drawdown_pct"].max()
    return max_dd

#extract and store historical data in dataframe
historicalData = hist_data(tickers, limit=1000)

    
#####################################   BACKTESTING   ##################################
ohlc_dict = deepcopy(historicalData)
stoch_signal = {}
tickers_signal = {}
tickers_ret = {}
trade_count = {}
trade_data = {}
hwm = {}

MACD(ohlc_dict)
stochastic(ohlc_dict)

for ticker in tickers.split(","):
    ohlc_dict[ticker].dropna(inplace=True)
    stoch_signal[ticker] = ""
    tickers_signal[ticker] = ""
    trade_count[ticker] = 0
    hwm[ticker] = 0
    tickers_ret[ticker] = [0]
    trade_data[ticker] = {}

for ticker in tickers.split(","):
    print("Calculating daily returns for ",ticker)
    for i in range(1,len(ohlc_dict[ticker])-1):
        if ohlc_dict[ticker]["%K"][i] < 20:
            stoch_signal[ticker] = "oversold"
        elif ohlc_dict[ticker]["%K"][i] > 80:
            stoch_signal[ticker] = "overbought"
        
        if tickers_signal[ticker] == "":
            tickers_ret[ticker].append(0)
            if ohlc_dict[ticker]["macd"][i]> ohlc_dict[ticker]["signal"][i] and \
               ohlc_dict[ticker]["macd"][i-1]< ohlc_dict[ticker]["signal"][i-1] and \
               stoch_signal[ticker]=="oversold":
                   tickers_signal[ticker] = "Buy"
                   trade_count[ticker]+=1
                   trade_data[ticker][trade_count[ticker]] = [ohlc_dict[ticker]["open"][i+1]]
                   hwm[ticker] = ohlc_dict[ticker]["open"][i+1]
                     
        elif tickers_signal[ticker] == "Buy":
            if ohlc_dict[ticker]["low"][i]<0.985*hwm[ticker]:
                tickers_signal[ticker] = ""
                trade_data[ticker][trade_count[ticker]].append(0.985*hwm[ticker])
                trade_count[ticker]+=1
                tickers_ret[ticker].append((0.985*hwm[ticker]/ohlc_dict[ticker]["close"][i-1])-1)
            else:
                hwm[ticker] = max(hwm[ticker],ohlc_dict[ticker]["high"][i])
                tickers_ret[ticker].append((ohlc_dict[ticker]["close"][i]/ohlc_dict[ticker]["close"][i-1])-1)
    
    if trade_count[ticker] % 2 != 0:
        trade_data[ticker][trade_count[ticker]].append(ohlc_dict[ticker]["close"][i+1])
        
    tickers_ret[ticker].append(0)
    ohlc_dict[ticker]["ret"] = np.array(tickers_ret[ticker])
    
    
# calculating overall strategy's KPIs
strategy_df = pd.DataFrame()
for ticker in tickers.split(","):
    strategy_df[ticker] = ohlc_dict[ticker]["ret"]
    strategy_df[ticker].fillna(0, inplace=True)
strategy_df["ret"] = strategy_df.mean(axis=1)
    

CAGR(strategy_df)
sharpe(strategy_df, 0.03)
max_dd(strategy_df)

(1+strategy_df["ret"]).cumprod().plot() #plotting cumulative strategy return

#calculating individual stock's KPIs
cagr = {}
sharpe_ratios = {}
max_drawdown = {}

for ticker in tickers.split(","):
    cagr[ticker] = CAGR(ohlc_dict[ticker])
    sharpe_ratios[ticker] =  sharpe(ohlc_dict[ticker],0.03)
    max_drawdown[ticker] =  max_dd(ohlc_dict[ticker])
    
KPI_df = pd.DataFrame([cagr,sharpe_ratios,max_drawdown],index=["Return","Sharpe Ratio","Max Drawdown"])      
KPI_df = KPI_df.T

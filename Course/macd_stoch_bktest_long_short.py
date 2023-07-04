import requests
import os
import json
import pandas as pd
from copy import deepcopy
import numpy as np

os.chdir("D:\Course")

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

#extract and store historical data in dataframe
historicalData = hist_data(tickers, limit=1000)

    
#####################################   BACKTESTING   ##################################
ohlc_dict = deepcopy(historicalData)
stoch_signal = {}
tickers_signal = {}
tickers_ret = {}
trade_count = {}
long_data = {}
short_data = {}
hwm = {}

stochastic(ohlc_dict)
MACD(ohlc_dict)

for ticker in tickers.split(","):
    print("Calculating MACD & Stochastics for ",ticker)
    ohlc_dict[ticker].dropna(inplace=True)
    stoch_signal[ticker] = ""
    trade_count[ticker] = 0
    tickers_signal[ticker] = ""
    hwm[ticker] = 0
    tickers_ret[ticker] = [0]
    long_data[ticker] = {}
    short_data[ticker] = {}
    
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
                   long_data[ticker][trade_count[ticker]] = [ohlc_dict[ticker]["open"][i+1]]
                   hwm[ticker] = ohlc_dict[ticker]["open"][i+1]
            elif ohlc_dict[ticker]["macd"][i]< ohlc_dict[ticker]["signal"][i] and \
               ohlc_dict[ticker]["macd"][i-1]> ohlc_dict[ticker]["signal"][i-1] and \
               stoch_signal[ticker]=="overbought":
                   tickers_signal[ticker] = "Sell"
                   trade_count[ticker]+=1
                   short_data[ticker][trade_count[ticker]] = [ohlc_dict[ticker]["open"][i+1]]
                   hwm[ticker] = ohlc_dict[ticker]["open"][i+1]
                     
        elif tickers_signal[ticker] == "Buy":
            if ohlc_dict[ticker]["low"][i]<0.985*hwm[ticker]:
                tickers_signal[ticker] = ""
                long_data[ticker][trade_count[ticker]].append(0.985*hwm[ticker])
                trade_count[ticker]+=1
                tickers_ret[ticker].append((0.985*hwm[ticker]/ohlc_dict[ticker]["close"][i-1])-1)
            else:
                hwm[ticker] = ohlc_dict[ticker]["high"][i]
                tickers_ret[ticker].append((ohlc_dict[ticker]["close"][i]/ohlc_dict[ticker]["close"][i-1])-1)
                
        elif tickers_signal[ticker] == "Sell":
            if ohlc_dict[ticker]["high"][i]>1.015*hwm[ticker]:
                tickers_signal[ticker] = ""
                short_data[ticker][trade_count[ticker]].append(1.015*hwm[ticker])
                trade_count[ticker]+=1
                tickers_ret[ticker].append((ohlc_dict[ticker]["close"][i-1]/1.015*hwm[ticker])-1)
            else:
                hwm[ticker] = ohlc_dict[ticker]["low"][i]
                tickers_ret[ticker].append((ohlc_dict[ticker]["close"][i-1]/ohlc_dict[ticker]["close"][i])-1)
                            
    if trade_count[ticker]%2 != 0:
        for trade in long_data[ticker]:
            if len(long_data[ticker][trade]) == 1:
                long_data[ticker][trade].append(ohlc_dict[ticker]["close"][i])
        for trade in short_data[ticker]:
            if len(short_data[ticker][trade]) == 1:
                short_data[ticker][trade].append(ohlc_dict[ticker]["close"][i])

    
    tickers_ret[ticker].append(0) #since we are removing the last row
    ohlc_dict[ticker]["ret"] = np.array(tickers_ret[ticker])

# calculating overall strategy's KPIs
long_df = {}
short_df = {}
return_df = {}

overall_return = 0
for ticker in tickers.split(","):
    try:
        long_df[ticker] = pd.DataFrame(long_data[ticker]).T
        long_df[ticker].columns = ["long_entry_pr","long_exit_pr"]
        long_df[ticker]["return"] = long_df[ticker]["long_exit_pr"]/long_df[ticker]["long_entry_pr"]
    except:
        print("no long trades for ", ticker)
    try:
        short_df[ticker] = pd.DataFrame(short_data[ticker]).T
        short_df[ticker].columns = ["short_entry_pr","short_exit_pr"]
        short_df[ticker]["return"] = short_df[ticker]["short_entry_pr"]/short_df[ticker]["short_exit_pr"]
    except:
        print("no short trades for ", ticker)
    
    if len(long_df[ticker]) == 0:
        return_df[ticker] = short_df[ticker]["return"]
    elif len(short_df[ticker]) == 0:
        return_df[ticker] = long_df[ticker]["return"]
    else:
        return_df[ticker] = long_df[ticker]["return"].append(short_df[ticker]["return"]).sort_index()   
    print("total return {} = {}".format(ticker,return_df[ticker].cumprod().iloc[-1]- 1))
    overall_return+= (1/len(tickers.split(",")))*(return_df[ticker].cumprod().iloc[-1]- 1)

print("Overall Return of Strategy = {}".format(overall_return))
  
#calculating individual stock's KPIs
win_rate = {}
mean_ret_pt = {}
mean_ret_pwt = {}
mean_ret_plt = {}
max_cons_loss = {}
for ticker in tickers.split(","):
    print("calculating intraday KPIs for ",ticker)
    win_rate[ticker] =  winRate(pd.DataFrame(return_df[ticker],columns=["return"]))      
    mean_ret_pt[ticker] =  meanretpertrade(pd.DataFrame(return_df[ticker],columns=["return"]))
    mean_ret_pwt[ticker] =  meanretwintrade(pd.DataFrame(return_df[ticker],columns=["return"]))
    mean_ret_plt[ticker] =  meanretlostrade(pd.DataFrame(return_df[ticker],columns=["return"]))
    max_cons_loss[ticker] =  maxconsectvloss(pd.DataFrame(return_df[ticker],columns=["return"]))

KPI_df = pd.DataFrame([win_rate,mean_ret_pt,mean_ret_pwt,mean_ret_plt,max_cons_loss],
                      index=["Win Rate","Mean Return Per Trade","MR Per WR", "MR Per LR", "Max Cons Loss"])      
KPI_df.T
 
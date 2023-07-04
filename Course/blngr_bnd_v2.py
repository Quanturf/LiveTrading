import os
import json
from alpaca_trade_api.rest import REST, TimeFrame

os.chdir("D:\Course")

endpoint = "https://data.alpaca.markets/v2"
headers = json.loads(open("key.txt",'r').read())

def hist_data(symbols, start_date ="2021-12-01", timeframe="Minute"):
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
        
data_dump = hist_data(["FB","CSCO","AMZN"], start_date ="2021-12-15", timeframe="Hour") 


def bollBand(df_dict, n=20):
    "function to calculate Bollinger Band"
    for df in df_dict:
        df_dict[df]["MB"] = df_dict[df]["close"].rolling(n).mean()
        df_dict[df]["UB"] = df_dict[df]["MB"] + 2*df_dict[df]["close"].rolling(n).std(ddof=0) #ddof=0 is required since we want to take the standard deviation of the population and not sample
        df_dict[df]["LB"] = df_dict[df]["MB"] - 2*df_dict[df]["close"].rolling(n).std(ddof=0) #ddof=0 is required since we want to take the standard deviation of the population and not sample
        df_dict[df]["BB_Width"] = df_dict[df]["UB"] -  df_dict[df]["LB"] 
        
print(bollBand(data_dump))
      
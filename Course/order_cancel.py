import requests
import os
import json
import pandas as pd

os.chdir("D:\Course")

endpoint = "https://paper-api.alpaca.markets"
headers = json.loads(open("key.txt",'r').read())

def limit_order(symbol, quantity, limit_pr, side="buy", tif="day"):
    ord_url = endpoint + "/v2/orders"
    params = {"symbol": symbol,
              "qty": quantity,
              "side" : side,
              "type": "limit",
              "limit_price" : limit_pr,
              "time_in_force": tif}
    r = requests.post(ord_url, headers=headers, json=params)
    return r.json()

def order_list(status = "open", limit = 50):
    ord_list_url = endpoint + "/v2/orders"
    params = {"status":status}
    r = requests.get(ord_list_url, headers=headers, params=params)
    data = r.json()
    return pd.DataFrame(data)

def order_cancel(order_id=""):
    if len(order_id)>1:
        ord_cncl_url = endpoint + "/v2/orders/{}".format(order_id)
    else:
        ord_cncl_url = endpoint + "/v2/orders"
    r = requests.delete(ord_cncl_url, headers=headers)
    return r.json()

order_df = order_list()
limit_order("AAPL", 15, 50, side="sell")
limit_order("MSFT", 10, 40)
order_cancel(order_df[order_df["symbol"]=="AAPL"]["id"].to_list()[0])
print(order_cancel())
    
import requests
import os
import json
import pandas as pd

os.chdir("D:\Course")

endpoint = "https://paper-api.alpaca.markets"
headers = json.loads(open("key.txt",'r').read())

def trail_stop_order(symbol, quantity, trail_pr, side="buy", tif="day"):
    ord_url = endpoint + "/v2/orders"
    params = {"symbol": symbol,
              "qty": quantity,
              "side" : side,
              "type": "trailing_stop",
              "trail_price" : trail_pr,
              "time_in_force": tif}
    r = requests.post(ord_url, headers=headers, json=params)
    return r.json()

def order_list(status = "open", limit = 50):
    ord_list_url = endpoint + "/v2/orders"
    params = {"status":status}
    r = requests.get(ord_list_url, headers=headers, params=params)
    data = r.json()
    return pd.DataFrame(data)

def order_replace(order_id, params):
    ord_replc_url = endpoint + "/v2/orders/{}".format(order_id)
    r = requests.patch(ord_replc_url, headers=headers, json=params)
    return r.json()

print(trail_stop_order("AAPL", 5, 2, "sell"))
order_df = order_list()
print(order_replace(order_df[order_df["symbol"]=="AAPL"]["id"].to_list()[0],
              {"qty" : 10, "trail": 3}))
    
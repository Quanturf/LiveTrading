import requests
import os
import json
import pandas as pd

os.chdir("D:\Course")

endpoint = "https://paper-api.alpaca.markets"
headers = json.loads(open("key.txt",'r').read())

def order_list(status = "open", limit = 50):
    ord_list_url = endpoint + "/v2/orders"
    params = {"status":status}
    r = requests.get(ord_list_url, headers=headers, params=params)
    data = r.json()
    return pd.DataFrame(data)

order_df = order_list("closed")
print(order_df)
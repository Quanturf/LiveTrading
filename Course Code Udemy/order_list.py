"""
Alpaca API - Orders API (Getting Order List)

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

import requests
import os
import json
import pandas as pd

os.chdir("D:\\Alpaca") #change this based on the path on your local machine

endpoint = "https://paper-api.alpaca.markets"
headers = json.loads(open("key.txt",'r').read())

def order_list(status = "open", limit = 50):
    ord_list_url = endpoint + "/v2/orders"
    params = {"status":status}
    r = requests.get(ord_list_url, headers=headers, params=params)
    data = r.json()
    return pd.DataFrame(data)

order_df = order_list("closed")
"""
Alpaca API - Getting account information

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

import requests
import os
import json

os.chdir("D:\\Alpaca") #change this based on the path on your local machine

endpoint = "https://paper-api.alpaca.markets"
headers = json.loads(open("key.txt",'r').read())

def get_account():
    acc_url = endpoint + "/v2/account"
    r = requests.get(acc_url,headers=headers)
    return r.json()

get_account() #get exhasutive information about your account
get_account()["equity"] #get only the relavant account information
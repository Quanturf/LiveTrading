import requests
import os
import json

os.chdir("D:\Course")

endpoint = "https://paper-api.alpaca.markets"
headers = json.loads(open("key.txt",'r').read())

def positions(symbol=""):
    if len(symbol)>1:
        pos_url = endpoint + "/v2/positions/{}".format(symbol)
    else:
        pos_url = endpoint + "/v2/positions"
    r = requests.get(pos_url, headers=headers)
    return r.json()

print(positions())
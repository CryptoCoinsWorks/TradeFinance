from pprint import pprint
import yfinance as yf
import json
import os
from modules.yahoo_fin import stock_info as sf


ticker = "AI.PA"

ticker = yf.Ticker(ticker)
sectreur = ticker.info['industry']

# industry
SCRIPT_PATH = os.path.dirname(__file__)
with open(os.path.join(SCRIPT_PATH, "data", "dataset.json"), "r") as f:
    x = json.load(f)

with open(os.path.join(SCRIPT_PATH, "data", "industries.json"), "r") as f:
    same = json.load(f)

cac = sf.tickers_cac()

# same = dict()

SCRIPT_PATH = os.path.dirname(__file__)
path = os.path.join(SCRIPT_PATH, "data", "industries.json")

for i, tick in enumerate(cac.keys()):
    # if i < 50:
    try:
        indus = yf.Ticker(tick).info['industry']
        # same.append(test)
        if indus not in same.keys():
            same[indus] = []
        same[indus].append(tick)
        with open(path, "w") as f:
            json.dump(same, f, indent=4)
    except:
        print('Error : ' + tick)

print('end')
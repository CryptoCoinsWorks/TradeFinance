from pprint import pprint
import yfinance as yf
import os
import requests
import re
import json
import pickle
from utils import constants as cst
from modules.yahoo_fin import stock_info as sf
from yahoofinancials import YahooFinancials
import pandas as pd

SCRIPT_PATH = os.path.dirname(__file__)
path = os.path.join(SCRIPT_PATH, "data", "sauve.json")

# test = [<pyqtgraph.graphicsItems.AxisItem.AxisItem(0x1738792cd90, parent=0x17387927620, pos=24,1, z=-1000, flags=(ItemStacksBehindParent|ItemUsesExtendedStyleOption|ItemSendsGeometryChanges|ItemNegativeZStacksBehindParent)) at 0x0000017402222500>]

#
# with open(path, "w") as f:
#     pickle.dump(test, f, indent=4)



quit()

with open(os.path.join(SCRIPT_PATH, "data", "industries.json"), "r") as f:
    same = json.load(f)


# x = sf.tickers_cac()
SCRIPT_PATH = os.path.dirname(__file__)
path = os.path.join(SCRIPT_PATH, "data", "industries.json")

for i, tick in enumerate(x.keys()):
    if 120 > i and i < 200:
        try:
            indus = yf.Ticker(tick).info['industry']
            # same.append(test)
            if indus not in same.keys():
                same[indus] = []
            if tick in same[indus]:
                print('pass')
                continue
            same[indus].append(tick)
            with open(path, "w") as f:
                json.dump(same, f, indent=4)
        except:
            print('Error : ' + tick)

print('end')
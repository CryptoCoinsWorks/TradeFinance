import talib
import pandas as pd
import numpy as np
import yfinance as yf
from pprint import pprint
import matplotlib.pyplot as plt

class PatternRecognizing(object):
    def __init__(self, data):


        plt.plot(data['Close'].values, color='black', label='Price')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.legend()
        # plt.show()



if __name__ == '__main__':
    tick = "GLE.PA"
    ticker = yf.Ticker(tick)
    data = ticker.history(period="1y", interval="1d", start="2008-01-01")
    pre = PatternRecognizing(data=data)

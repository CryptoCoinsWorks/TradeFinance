import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

DEV = True

TITLE = "TRADING VISUALISATION"

OPEN = "Open"
CLOSE = "Close"
ADJ_CLOSE = "Adj Close"
ADJ_CLOSE_LOW = "adjclose"
HIGH = "High"
LOW = "Low"
VOLUME = "Volume"

splashcreen = "resources\img\splashscreen.jpg"

TICKERS_MARKETS = {
    "NASDAQ": "%5EIXIC",
    "S&P 500": "%5EGSPC",
    "Dow Jones": "%5EDJI",
    "Oil": "CL%3DF",
    "BTC": "BTC-USD",
    "ETH": "ETH-USD",
    "EUR/USD": "EURUSD%3DX",
    "GBP/USD": "GBPUSD%3DX",
    "Gold": "GC%3DF",
}

TICKERS_SENTIMENTALS = ['TSLA', 'AAPL', 'MSFT', 'GLE.PA', 'FP.PA']

START_DATE = "2018-01-01"
PERIODE = "1y"
INTERVAL = "1d"
INTERVAL_MONTH = "1mo"

DATABASE = db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', "users.db")

AAA_YIELD_link = "https://ycharts.com/indicators/moodys_seasoned_aaa_corporate_bond_yield"

PRIVATE_KEY = 'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='

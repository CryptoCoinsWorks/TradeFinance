import os
import json
import random
import yfinance as yf
from pprint import pprint
from utils import constants as cst

def set_id():
    id = random.SystemRandom().randint(1, 999)
    if all_ids(id):
        set_id()
    return id

def all_ids(uiid):
    orders = load_orders()
    for order in orders:
        if uiid == order['id']:
            return True
        else:
            return False

def load_orders():
    """Load orders from the file

    :return: The loaded favorite
    :rtype: list
    """
    _app_home = os.environ.get("APP_HOME")
    path = os.path.join(
        _app_home, "orders", "orders.json"
    )
    order = []
    if not _check_orders(path):
        create_order(path)
        return order
    with open(path, "r") as f:
        order = json.load(f)
    return order

def create_order(orders_path) -> bool:
    """Create the order file if it doesn't exists

    :return: True if exists, False if the creation failed
    :rtype: bool
    """
    if not os.path.exists(os.path.dirname(orders_path)):
        try:
            os.mkdir(os.path.dirname(orders_path))
        except Exception as error:  # TODO cath correct error
            print(error)
    # create file in all cases
    try:
        with open(orders_path, "w") as f:
            json.dump(list(), f, indent=4)
            f.close()
    except Exception as error:
        print(error)
        return False
    return True

def save_orders(orders):
    _app_home = os.environ.get("APP_HOME")
    path = os.path.join(
        _app_home, "orders", "orders.json"
    )
    with open(path, "w") as f:
        json.dump(orders, f, indent=4)


def _check_orders(path):
    """Check if the file exists

    :return: True or False
    :rtype: bool
    """
    if os.path.exists(path):
        return True
    return False


def get_last_price(ticker):
    """Return the last current price from a ticker
    """
    ticker = yf.Ticker(ticker)
    data = ticker.history(period="1y", interval="1d", start=cst.START_DATE)
    return data[cst.CLOSE].iloc[-1]


def check_ticker_orders(ticker):
    positions = list()
    orders = load_orders()
    for position in orders:
        if position['ticker'] == ticker:
            positions.append(position)
    return positions

def get_position_by_id(id):
    orders = load_orders()
    for order in orders:
        if str(order['id']) == str(id):
            return order

def modify_order(data):
    orders = load_orders()
    for index, i in enumerate(orders):
        if i['id'] == data['id']:
            orders.pop(index)
    orders.append(data)
    save_orders(orders)
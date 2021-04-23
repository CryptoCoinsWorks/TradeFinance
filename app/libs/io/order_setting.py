import os
import json
from utils import utils_orders
from PySide2 import QtCore
from libs.events_handler import EventHandler


class OrderSettings(QtCore.QObject):
    def __init__(self, parent=None):
        super(OrderSettings, self).__init__(parent)

        # Constants
        self._app_home = os.environ.get("APP_HOME")
        self._orders_path = os.path.join(
            self._app_home, "orders", "orders.json"
        )
        self.signals = EventHandler()

    def load_position(self):
        self.orders = utils_orders.load_orders()
        self.signals.sig_order_loaded.emit(self.orders)

    QtCore.Signal(dict)
    def save_orders(self, order):
        order["id"] = utils_orders.set_id()
        self.orders.append(order)
        self._save_orders()

    def _save_orders(self):
        """Save favorites into the file"""
        if not utils_orders._check_orders(self._orders_path):
            utils_orders.create_order(self._orders_path)
        with open(self._orders_path, "w") as f:
            json.dump(self.orders, f, indent=4)

    QtCore.Slot(int)
    def close_order(self, id):
        """This method delete the position from the file.
        """
        self.orders = utils_orders.load_orders()
        for index, i in enumerate(self.orders):
            if i['id'] == id:
                self.orders.pop(index)
        self._save_orders()

def get_profits(position):
    price = utils_orders.get_last_price(position['ticker'])
    buy_price = round(position['price'], 2)
    profit = float(buy_price) - float(price)
    return profit



import os
import json

from utils import utils
from pprint import pprint
from PySide2 import QtCore
from libs.events_handler import EventHandler


class OrderSettings(QtCore.QObject):
    def __init__(self, parent=None):
        super(OrderSettings, self).__init__(parent)

        # Constants
        self.signals = EventHandler()
        self._app_home = os.environ.get("APP_HOME")
        self._orders_path = os.path.join(
            self._app_home, "orders", "orders.json"
        )
        self.orders = self.load_orders()
        self.signals.sig_order_added.connect(
            self.save_orders
        )
        self.signals.sig_order_close.connect(
            self.close_order
        )

    def load_orders(self) -> list:
        """Load orders from the file

        :return: The loaded favorite
        :rtype: list
        """
        self.orders = []
        if not self._check_orders():
            return self.orders
        with open(self._orders_path, "r") as f:
            self.orders = json.load(f)
        return self.orders

    QtCore.Signal(dict)

    def save_orders(self, order):
        order["id"] = utils.set_id()
        self.orders.append(order)
        self._save_orders()

    def _save_orders(self):
        """Save favorites into the file"""
        if not self._check_orders():
            self.create_order()
        with open(self._orders_path, "w") as f:
            json.dump(self.orders, f, indent=4)
        # self.signals.sig_favorite_saved.emit(self._favorites)

    def create_order(self) -> bool:
        """Create the order file if it doesn't exists

        :return: True if exists, False if the creation failed
        :rtype: bool
        """
        if not os.path.exists(os.path.dirname(self._orders_path)):
            try:
                os.mkdir(os.path.dirname(self._orders_path))
            except Exception as error:  # TODO cath correct error
                print(error)
        # create file in all cases
        try:
            open(self._orders_path, "w").close()
        except Exception as error:
            print(error)
            return False
        # self.signals.sig_favorite_created.emit(self._favorites)
        return True

    def _check_orders(self):
        """Check if the favorite file exists

        :return: True or False
        :rtype: bool
        """
        if os.path.exists(self._orders_path):
            return True
        return False

    QtCore.Slot(int)
    def close_order(self, id):
        print('id', id)
        self.orders = self.load_orders()
        for index, i in enumerate(self.orders):
            if i['id'] == id:
                self.orders.pop(index)
        self._save_orders()

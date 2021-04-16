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
        self._app_home = os.environ.get("APP_HOME")
        self._orders_path = os.path.join(
            self._app_home, "orders", "orders.json"
        )
        self.signals = EventHandler()

    def load_position(self):
        self.orders = utils.load_orders(self._orders_path)
        self.signals.sig_order_loaded.emit(self.orders)

    QtCore.Signal(dict)
    def save_orders(self, order):
        order["id"] = utils.set_id()
        self.orders.append(order)
        self._save_orders()

    def _save_orders(self):
        """Save favorites into the file"""
        if not utils._check_orders(self._orders_path):
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

    QtCore.Slot(int)
    def close_order(self, id):
        """This method delete the position from the file.
        """
        self.orders = utils.load_orders(self._orders_path)
        for index, i in enumerate(self.orders):
            if i['id'] == id:
                self.orders.pop(index)
        self._save_orders()

import os
import json
from utils import constants as cst
from utils import utils_orders
from utils import db_models
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
        self.db_connection = db_models.connection_to_db(cst.DATABASE)

    def load_position(self):
        self.orders = db_models.get_positions(self.db_connection)
        self.signals.sig_order_loaded.emit(self.orders)

    QtCore.Signal(dict)
    def save_orders(self, order):
        self.orders.append(order)
        id_db = db_models.create_position(self.db_connection, order)
        order = db_models.get_position_by_id(self.db_connection, id_db)
        self.signals.sig_order_create.emit(order)

    QtCore.Slot(int)
    def close_order(self, id):
        """This method delete the position from the file.
        """
        db_models.close_position(self.db_connection, id=id)

def get_profits(position):
    price = utils_orders.get_last_price(position[1])
    buy_price = round(position[5], 2)
    profit = float(buy_price) - float(price)
    return profit



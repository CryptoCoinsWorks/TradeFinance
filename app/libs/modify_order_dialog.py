from PySide2 import QtGui, QtCore, QtWidgets
from libs.events_handler import EventHandler
from utils import utils_orders
from utils import constants as cst
from ui.order_modify_widget import Ui_Dialog
from utils import db_models


class ModifyOrderDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None, position=None):
        super(ModifyOrderDialog, self).__init__(parent)

        self.setupUi(self)
        self.signal = EventHandler()
        self.first = False
        self.position = dict()

        self.id = position[1].data(QtCore.Qt.DisplayRole)
        self.ticker = position[0].data(QtCore.Qt.DisplayRole)
        self.stop_l = position[5].data(QtCore.Qt.DisplayRole)
        self.take_p = position[6].data(QtCore.Qt.DisplayRole)
        self.price = utils_orders.get_last_price(ticker=self.ticker)

        self.button_modify.clicked.connect(self.get_data)
        self.lb_ticker.setText(self.ticker)
        self._change_box()

        self.get_dict()

    def get_dict(self):
        """This method create a dict of
            the position from order.json
        """
        db_connection = db_models.connection_to_db(cst.DATABASE)
        self.position = db_models.find_position_from_id(db_connection=db_connection, id=self.id)

    def get_data(self):
        """This method get the value from the QDoubleBox
            Then close the window.
        """
        stop_loss = self.box_stop.value()
        take_profit = self.box_profit.value()
        position = list(self.position)
        position[9] = take_profit
        position[10] = stop_loss
        self.position = tuple(position)
        self.close()

    def _change_box(self):
        self.box_profit.setValue(self.price-1)
        self.box_stop.setValue(self.price-1)

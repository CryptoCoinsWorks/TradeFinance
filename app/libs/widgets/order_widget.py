import datetime
import numpy as np
from utils import utils
from pprint import pprint
from ui.order import Ui_Form
from PySide2 import QtCore, QtWidgets, QtGui
from libs.events_handler import EventHandler


style_hide = "background-color:rgb(90,90,90);"

class OrderView(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None, data=None):
        super(OrderView, self).__init__(parent=parent)

        self.signals = EventHandler()

        self.setupUi(self)
        self.order_wgt.setStyleSheet('background-color: rgb(43, 43, 43);')

        # Constants
        self.buy = False
        self.sell = False
        self.data = None
        self.ticker = None

        self.buy_btn.clicked.connect(self.set_buy)
        self.sell_btn.clicked.connect(self.set_sell)
        self.btn_order.clicked.connect(self.place_order)

        self.set_ui()

    def set_ui(self):
        self.buy_btn.setStyleSheet(style_hide)
        self.sell_btn.setStyleSheet(style_hide)
        self.btn_order.setStyleSheet(style_hide)

    def set_buy(self):
        active = "background-color:green;"
        self.buy_btn.setStyleSheet(active)
        self.sell_btn.setStyleSheet(style_hide)
        self.btn_order.setStyleSheet(active)
        self.btn_order.setText("PLACE BUY ORDER")
        self.buy = True
        self.sell = False

    def set_sell(self):
        active = "background-color:red;"
        self.buy_btn.setStyleSheet(style_hide)
        self.sell_btn.setStyleSheet(active)
        self.btn_order.setStyleSheet(active)
        self.btn_order.setText("PLACE SELL ORDER")
        self.buy = False
        self.sell = True

    @QtCore.Slot(str, dict)
    def get_data(self, ticker, data):
        """Get prices by the signal emit from the ticker.
        """
        self.data = data
        self.price = data.iloc[-1]['Close']
        self.ticker = ticker

    def place_order(self):
        """Place Order.
        Check the current Tab to know what kind of order.
        """
        current_bar = self.order_wgt.currentIndex()
        if current_bar == 0:
            self._order_market(order_exec="MARKET")
        elif current_bar == 1:
            self._order_limit(order_exec="LIMIT")
        elif current_bar == 2:
            self._order_stop(order_exec="STOP")

    def _order_market(self, order_exec):
        """Buy or Sell at market price.
        """
        total = 0
        amount = 0

        if self.buy:
            order_type = "BUY"
            amount = self.box_quantity_market.value()
            total = amount * self.price

        elif self.sell:
            order_type = "SELL"
            amount = self.box_quantity_market.value()
            total = amount * self.price

        else:
            return

        self.set_total(total=total)
        self._build_order(amount=amount, order_type=order_type, order_exec=order_exec)

    def _order_limit(self, order_exec):
        pass

    def _order_stop(self, order_exec):
        pass

    def set_total(self, total=0):
        self.lb_price.setText("%s €" % total)

    def _build_order(self, amount, order_type, order_exec, limit="", stop="", timing=""):
        order = {
            "ticker": self.ticker,
            "order_type": order_type,
            "order_execution": order_exec,
            "amount": amount,
            "price": self.price,
            "limit": limit,
            "stop": stop,
            "date": datetime.datetime.now().timestamp(),
            "timing": timing,
        }
        self.signals.sig_order_added.emit(order)


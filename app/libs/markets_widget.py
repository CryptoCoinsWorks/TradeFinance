import numpy as np
from ui import markets_widget
from PySide2 import QtWidgets
from utils import constants as cst
from modules.yahoo_fin import stock_info
from libs.thread_pool import ThreadPool
from libs.events_handler import EventHandler
from libs.widgets.stackedwidget import StackedWidget


class MarketsWidget(StackedWidget):
    """
    Markets are the informations in the Welcome Page showing price and
    variation from day before.
    """

    def __init__(self, parent=None):
        super(MarketsWidget, self).__init__(parent)

        self.signal = EventHandler()
        self.thread_pool = ThreadPool()

        page = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(page)

        if not cst.DEV:
            for count, (name, tick) in enumerate(cst.TICKERS_MARKETS.items()):
                if count % 5 == 0:
                    page = QtWidgets.QWidget()
                    layout = QtWidgets.QHBoxLayout(page)
                item = MarketsWidgetItem(self, ticker=tick, compagny=name)
                layout.addWidget(item)

                self.addWidget(page)


class MarketsWidgetItem(QtWidgets.QWidget, markets_widget.Ui_markets):
    def __init__(self, parent=None, ticker=None, compagny=None):
        super(MarketsWidgetItem, self).__init__(parent)

        self.setupUi(self)
        try:
            stock = stock_info.get_data(ticker)
        except:
            return

        day = float(stock[cst.ADJ_CLOSE_LOW][-1])
        prev_day = float(stock[cst.ADJ_CLOSE_LOW][-2])

        if np.isnan(prev_day):
            if not np.isnan(stock[cst.ADJ_CLOSE_LOW][-3]):
                prev_day = float(stock[cst.ADJ_CLOSE_LOW][-3])
            else:
                prev_day = float(stock[cst.ADJ_CLOSE_LOW][-4])

        variation = ((day - prev_day) / prev_day) * 100
        variation = round(variation, 2)

        self.title.setText(compagny)
        self.price.setText("{} €".format(str(round(day, 2))))
        self.pourcentage.setText("{}%".format(str(variation)))

        if variation <= 0:
            self.pourcentage.setStyleSheet("color:rgb(239, 83, 80);")
        else:
            self.pourcentage.setStyleSheet("color:rgb(38, 166, 154);")
